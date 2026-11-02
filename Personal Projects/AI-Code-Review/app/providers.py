"""Local Ollama model providers with health checks, bounded retries and
primary -> fallback routing. No cloud provider exists in this module by design."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import requests

from app.review_schema import InvalidModelOutput

log = logging.getLogger(__name__)


class ProviderError(Exception):
    """Base class for failures classified by the provider."""


class ProviderUnavailable(ProviderError):
    """Ollama is unreachable or the model is missing / failed to load."""


class ProviderTimeout(ProviderError):
    """Generation exceeded the configured timeout."""


class AllModelsFailed(Exception):
    def __init__(self, failures):
        self.failures = list(failures)
        super().__init__("; ".join(self.failures) or "no model available")


def model_present(name: str, available) -> bool:
    available = set(available)
    return name in available or (":" not in name and f"{name}:latest" in available)


class OllamaProvider:
    def __init__(self, settings, model: str, session=None, sleep=time.sleep):
        self.settings = settings
        self.model = model
        self.http = session or requests
        self.sleep = sleep
        self.verified = False

    def _url(self, path: str) -> str:
        return f"{self.settings.ollama_base_url}{path}"

    def check_available(self) -> None:
        """Verify the server is up and the model is installed (never pulls models)."""
        try:
            resp = self.http.get(self._url("/api/tags"), timeout=self.settings.connect_timeout)
            resp.raise_for_status()
            names = {m.get("name", "") for m in resp.json().get("models", [])}
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise ProviderUnavailable(f"Ollama not reachable at {self.settings.ollama_base_url}") from exc
        except (requests.RequestException, ValueError) as exc:
            raise ProviderUnavailable(f"Ollama health check failed: {exc}") from exc
        if not model_present(self.model, names):
            raise ProviderUnavailable(f"model '{self.model}' is not installed locally")
        self.verified = True

    def _generate_once(self, prompt: str) -> str:
        s = self.settings
        try:
            resp = self.http.post(
                self._url("/api/generate"),
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": s.temperature, "num_ctx": s.num_ctx},
                },
                timeout=(s.connect_timeout, s.generate_timeout),
            )
        except requests.ReadTimeout as exc:
            raise ProviderTimeout(f"{self.model}: generation timed out") from exc
        except (requests.ConnectionError, requests.Timeout) as exc:
            raise ProviderUnavailable(f"{self.model}: connection failed") from exc
        if resp.status_code == 404:
            raise ProviderUnavailable(f"{self.model}: model not found")
        if resp.status_code >= 500:
            raise ProviderUnavailable(f"{self.model}: server error {resp.status_code}")
        if resp.status_code >= 400:
            raise ProviderError(f"{self.model}: request rejected ({resp.status_code})")
        try:
            return resp.json()["response"]
        except (ValueError, KeyError) as exc:
            raise InvalidModelOutput(f"{self.model}: malformed Ollama response") from exc

    def generate(self, prompt: str, parse):
        """Generate and validate. Transient connection errors and invalid output are
        retried (bounded, exponential backoff); timeouts are not retried."""
        attempts = self.settings.max_retries + 1
        for attempt in range(attempts):
            try:
                return parse(self._generate_once(prompt))
            except ProviderTimeout:
                raise
            except (ProviderUnavailable, InvalidModelOutput):
                if attempt == attempts - 1:
                    raise
                delay = self.settings.retry_backoff * (2 ** attempt)
                log.warning("%s: attempt %d failed, retrying in %.1fs", self.model, attempt + 1, delay)
                self.sleep(delay)


@dataclass
class GenerationResult:
    parsed: object
    model: str
    failures: list = field(default_factory=list)


class ModelRouter:
    """Try providers in priority order (primary, then fallback)."""

    def __init__(self, providers):
        self.providers = list(providers)
        self._unavailable: dict = {}

    def generate(self, prompt: str, parse) -> GenerationResult:
        failures = []
        for provider in self.providers:
            if provider.model in self._unavailable:
                failures.append(f"{provider.model}: skipped ({self._unavailable[provider.model]})")
                continue
            try:
                if not provider.verified:
                    provider.check_available()
                parsed = provider.generate(prompt, parse)
                if failures:
                    log.warning("fell back to %s after: %s", provider.model, "; ".join(failures))
                return GenerationResult(parsed, provider.model, failures)
            except ProviderUnavailable as exc:
                self._unavailable[provider.model] = str(exc)
                failures.append(str(exc))
            except (ProviderTimeout, InvalidModelOutput, ProviderError) as exc:
                failures.append(f"{provider.model}: {exc}")
            log.warning("model %s failed: %s", provider.model, failures[-1])
        raise AllModelsFailed(failures)


def build_router(settings, session=None, sleep=time.sleep) -> ModelRouter:
    models = [settings.primary_model]
    if settings.fallback_model and settings.fallback_model != settings.primary_model:
        models.append(settings.fallback_model)
    return ModelRouter([OllamaProvider(settings, m, session, sleep) for m in models])
