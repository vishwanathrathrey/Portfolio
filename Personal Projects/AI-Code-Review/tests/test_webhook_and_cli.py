import hashlib
import hmac
import json

import pytest

import webhook_server as ws
from app.config import load_settings
from run_review import main, pr_from_event

SECRET = "s3cret-value"


def sign(body: bytes, secret=SECRET):
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv("GITHUB_WEBHOOK_SECRET", SECRET)
    ws._seen.clear()
    submitted = []
    monkeypatch.setattr(ws._executor, "submit", lambda fn, *a: submitted.append(a))
    return submitted


def post(body: dict, event="pull_request", sig=None, delivery="d-1"):
    raw = json.dumps(body).encode()
    headers = {"X-GitHub-Event": event, "X-GitHub-Delivery": delivery,
               "X-Hub-Signature-256": sig if sig is not None else sign(raw),
               "Content-Type": "application/json"}
    return ws.app.test_client().post("/webhook", data=raw, headers=headers)


PAYLOAD = {"action": "opened", "repository": {"full_name": "me/repo"}, "pull_request": {"number": 7}}


def test_signature_validation():
    body = b"{}"
    assert ws.is_valid_signature(body, sign(body), SECRET)
    assert not ws.is_valid_signature(body, sign(body, "other"), SECRET)
    assert not ws.is_valid_signature(body, None, SECRET)
    assert not ws.is_valid_signature(body, sign(body), "")      # no secret never validates


def test_unconfigured_secret_rejects_everything(monkeypatch):
    monkeypatch.delenv("GITHUB_WEBHOOK_SECRET", raising=False)
    monkeypatch.setattr("app.config.load_dotenv", lambda *a, **k: None)
    assert post(PAYLOAD).status_code == 503


def test_bad_signature_is_rejected_before_any_work(env):
    assert post(PAYLOAD, sig="sha256=bad").status_code == 401 and env == []


@pytest.mark.parametrize("action", ["opened", "synchronize", "reopened", "ready_for_review"])
def test_supported_pr_events_start_a_background_review(env, action):
    resp = post({**PAYLOAD, "action": action}, delivery=f"d-{action}")
    assert resp.status_code == 202 and env == [("me/repo", 7)]


@pytest.mark.parametrize("action", ["closed", "labeled", "edited", "converted_to_draft"])
def test_other_actions_are_ignored(env, action):
    assert post({**PAYLOAD, "action": action}).get_json() == {"status": "ignored"} and env == []


def test_ping_other_events_and_bad_payloads(env):
    assert post({}, event="ping").get_json() == {"status": "pong"}
    assert post(PAYLOAD, event="push").get_json() == {"status": "ignored"}
    assert post({"action": "opened"}).status_code == 400
    assert env == []


def test_redelivered_webhook_is_not_processed_twice(env):
    assert post(PAYLOAD).status_code == 202
    assert post(PAYLOAD).get_json() == {"status": "duplicate delivery"}
    assert len(env) == 1


# ----------------------------------------------------------------------- CLI
def write_event(tmp_path, action):
    path = tmp_path / "event.json"
    path.write_text(json.dumps({**PAYLOAD, "action": action, "pull_request": {"number": 9}}))
    return str(path)


def test_cli_reads_pr_from_actions_event(tmp_path):
    assert pr_from_event(write_event(tmp_path, "synchronize"))[0] == ("me/repo", 9)
    assert pr_from_event(write_event(tmp_path, "closed"))[0] is None


def test_cli_exit_codes(monkeypatch):
    from app.report_model import PRContext, ReviewResult
    ctx = PRContext("me/repo", 1, "", "", "", "", "", "")

    class Fake:
        def __init__(self, status, emailed=True):
            self.r = ReviewResult(ctx, status, email_delivered=emailed)

        def run(self, repo, number, force=False):
            return self.r

    for status, emailed, code in [("completed", True, 0), ("skipped", False, 0), ("duplicate", False, 0),
                                  ("failed", False, 1), ("completed", False, 2)]:
        monkeypatch.setattr("run_review.build_pipeline", lambda s, f=Fake(status, emailed): f)
        assert main(["--repo", "me/repo", "--pr", "1"]) == code


def test_settings_defaults_match_required_local_models():
    s = load_settings({})
    assert (s.primary_model, s.fallback_model, s.embedding_model, s.ollama_base_url) == (
        "qwen2.5-coder:7b", "mistral", "nomic-embed-text", "http://localhost:11434")
    custom = load_settings({"OLLAMA_PRIMARY_MODEL": "x:1", "OLLAMA_BASE_URL": "http://h:1/", "OLLAMA_MAX_RETRIES": "abc"})
    assert custom.primary_model == "x:1" and custom.ollama_base_url == "http://h:1" and custom.max_retries == 1
