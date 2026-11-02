import json

import pytest
import requests

from app.providers import (AllModelsFailed, ModelRouter, OllamaProvider, ProviderTimeout,
                           ProviderUnavailable, build_router, model_present)
from app.review_schema import parse_review
from tests.helpers import finding_json, make_settings


class Resp:
    def __init__(self, status=200, payload=None):
        self.status_code, self._payload = status, payload or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


class FakeOllama:
    """Scripted Ollama: installed models + per-model generate behaviour."""

    def __init__(self, installed, behaviour):
        self.installed, self.behaviour, self.calls = installed, behaviour, []

    def get(self, url, timeout=None):
        self.calls.append(("GET", url))
        if isinstance(self.installed, Exception):
            raise self.installed
        return Resp(200, {"models": [{"name": n} for n in self.installed]})

    def post(self, url, json=None, timeout=None):
        self.calls.append(("POST", url, json["model"]))
        action = self.behaviour[json["model"]]
        action = action.pop(0) if isinstance(action, list) else action
        if isinstance(action, Exception):
            raise action
        if isinstance(action, int):
            return Resp(action)
        return Resp(200, {"response": action})


def router(fake, **kw):
    sleeps = []
    return build_router(make_settings(**kw), session=fake, sleep=sleeps.append), sleeps


GOOD = finding_json()


def test_model_name_normalisation():
    assert model_present("mistral", {"mistral:latest"})
    assert model_present("qwen2.5-coder:7b", {"qwen2.5-coder:7b"})
    assert not model_present("qwen2.5-coder:3b", {"qwen2.5-coder:7b"})


def test_primary_model_is_used_first():
    fake = FakeOllama(["qwen2.5-coder:7b", "mistral:latest"], {"qwen2.5-coder:7b": GOOD, "mistral": GOOD})
    result = router(fake)[0].generate("p", parse_review)
    assert result.model == "qwen2.5-coder:7b"
    assert [c for c in fake.calls if c[0] == "POST"] == [("POST", "http://localhost:11434/api/generate", "qwen2.5-coder:7b")]


def test_missing_primary_falls_back_to_mistral_without_pulling_models():
    fake = FakeOllama(["mistral:latest"], {"mistral": GOOD})
    result = router(fake)[0].generate("p", parse_review)
    assert result.model == "mistral" and "not installed" in result.failures[0]
    assert not any("pull" in c[1] for c in fake.calls)             # never downloads models


def test_primary_timeout_is_not_retried_and_falls_back():
    fake = FakeOllama(["qwen2.5-coder:7b", "mistral:latest"],
                      {"qwen2.5-coder:7b": requests.ReadTimeout(), "mistral": GOOD})
    r, sleeps = router(fake)
    assert r.generate("p", parse_review).model == "mistral"
    assert sum(1 for c in fake.calls if c[0] == "POST" and c[2] == "qwen2.5-coder:7b") == 1
    assert sleeps == []


def test_invalid_output_is_retried_with_backoff_then_falls_back():
    fake = FakeOllama(["qwen2.5-coder:7b", "mistral:latest"],
                      {"qwen2.5-coder:7b": ["garbage", "still garbage"], "mistral": GOOD})
    r, sleeps = router(fake, max_retries=1, retry_backoff=2.0)
    assert r.generate("p", parse_review).model == "mistral"
    assert sleeps == [2.0]                                         # one bounded retry, backoff applied


def test_retries_are_bounded_and_backoff_is_exponential():
    fake = FakeOllama(["qwen2.5-coder:7b"], {"qwen2.5-coder:7b": [500, 500, 500, 500, 500]})
    r, sleeps = router(fake, max_retries=2, retry_backoff=1.0, fallback_model="")
    with pytest.raises(AllModelsFailed):
        r.generate("p", parse_review)
    assert sleeps == [1.0, 2.0]
    assert sum(1 for c in fake.calls if c[0] == "POST") == 3       # 1 try + 2 retries, never infinite


def test_ollama_down_fails_all_models_with_clear_reasons():
    fake = FakeOllama(requests.ConnectionError(), {})
    with pytest.raises(AllModelsFailed) as err:
        router(fake)[0].generate("p", parse_review)
    assert len(err.value.failures) == 2 and "not reachable" in err.value.failures[0]


def test_unavailable_model_is_checked_once_per_run():
    fake = FakeOllama(["mistral:latest"], {"mistral": GOOD})
    r, _ = router(fake)
    r.generate("p", parse_review)
    r.generate("p", parse_review)
    assert sum(1 for c in fake.calls if c[0] == "GET") == 2   # one health check per model, not per call
    assert "qwen2.5-coder:7b" in r._unavailable


def test_both_models_failing_raises_all_models_failed():
    fake = FakeOllama(["qwen2.5-coder:7b", "mistral:latest"],
                      {"qwen2.5-coder:7b": requests.ReadTimeout(), "mistral": requests.ReadTimeout()})
    with pytest.raises(AllModelsFailed):
        router(fake)[0].generate("p", parse_review)


def test_request_uses_json_format_and_configured_timeouts():
    captured = {}

    class Spy(FakeOllama):
        def post(self, url, json=None, timeout=None):
            captured.update(json=json, timeout=timeout)
            return Resp(200, {"response": GOOD})

    fake = Spy(["qwen2.5-coder:7b"], {})
    router(fake, generate_timeout=42.0, connect_timeout=3.0, num_ctx=4096)[0].generate("p", parse_review)
    assert captured["json"]["format"] == "json" and captured["json"]["options"]["num_ctx"] == 4096
    assert captured["timeout"] == (3.0, 42.0)


def test_no_cloud_provider_is_configured():
    import app.providers as providers
    source = open(providers.__file__, encoding="utf-8").read().lower()
    assert "anthropic" not in source and "openai" not in source
