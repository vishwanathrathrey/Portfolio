"""Async HTTP client for the local Ollama API."""

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.config import settings


class OllamaError(Exception):
    """An Ollama API request or response error."""

    def __init__(self, message: str, status_code: int | None = None, body: str = "") -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class OllamaClient:
    """A thin asynchronous wrapper around Ollama's HTTP API."""

    def __init__(self, base_url: str, timeout: float = 120.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @retry(
        stop=stop_after_attempt(settings.llm_max_retries),
        wait=wait_exponential(min=1, max=8),
        retry=retry_if_exception_type(OllamaError),
        reraise=True,
    )
    async def generate(
        self,
        model: str,
        prompt: str,
        *,
        system: str | None = None,
        format_json: bool = False,
        temperature: float = 0.2,
        num_predict: int = 1024,
    ) -> str:
        """Generate a non-streaming response from an Ollama model."""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json" if format_json else None,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict,
            },
            "system": system or "",
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(f"{self.base_url}/api/generate", json=payload)
        except httpx.HTTPError as error:
            raise OllamaError(f"Ollama request failed: {error}") from error

        if response.status_code != httpx.codes.OK:
            raise OllamaError(
                f"Ollama returned HTTP {response.status_code}.",
                status_code=response.status_code,
                body=response.text,
            )

        try:
            response_data: Any = response.json()
        except ValueError as error:
            raise OllamaError(
                "Ollama returned invalid JSON.",
                status_code=response.status_code,
                body=response.text,
            ) from error

        if not isinstance(response_data, dict) or not isinstance(
            response_data.get("response"), str
        ):
            raise OllamaError(
                "Ollama response did not include a string response field.",
                status_code=response.status_code,
                body=response.text,
            )
        return response_data["response"]

    async def list_models(self) -> list[str]:
        """Return the names of models reported by Ollama."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/api/tags")
        except httpx.HTTPError as error:
            raise OllamaError(f"Ollama request failed: {error}") from error

        if response.status_code != httpx.codes.OK:
            raise OllamaError(
                f"Ollama returned HTTP {response.status_code}.",
                status_code=response.status_code,
                body=response.text,
            )

        try:
            response_data: Any = response.json()
        except ValueError as error:
            raise OllamaError(
                "Ollama returned invalid JSON.",
                status_code=response.status_code,
                body=response.text,
            ) from error

        if not isinstance(response_data, dict) or not isinstance(
            response_data.get("models"), list
        ):
            raise OllamaError(
                "Ollama tags response did not include a models list.",
                status_code=response.status_code,
                body=response.text,
            )
        return [
            model["name"]
            for model in response_data["models"]
            if isinstance(model, dict) and isinstance(model.get("name"), str)
        ]

    async def health(self) -> bool:
        """Return whether Ollama can be reached without propagating errors."""
        try:
            await self.list_models()
        except OllamaError:
            return False
        return True


def get_ollama_client() -> OllamaClient:
    """Create an Ollama client for dependency injection."""
    return OllamaClient(
        base_url=settings.ollama_base_url,
        timeout=float(settings.llm_timeout_seconds),
    )
