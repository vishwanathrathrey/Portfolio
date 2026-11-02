import html

import pytest
import requests

from app.github_api import GitHubClient, GitHubError
from app.github_publisher import marker, publish_review
from app.models import ReviewFinding
from app.notifier import EmailNotifier, build_failure_email, build_report_email
from app.report_model import PRContext, ReviewResult
from app.state import MAX_ATTEMPTS, STALE_RUNNING_SECONDS, ReviewStore
from tests.helpers import FakeGitHub, make_settings


# ----------------------------------------------------------------- GitHub API
class R:
    def __init__(self, status=200, payload=None, headers=None):
        self.status_code, self._p, self.headers = status, payload if payload is not None else [], headers or {}

    def json(self):
        return self._p


class Session:
    def __init__(self, responses):
        self.responses, self.calls = list(responses), []

    def request(self, method, url, headers=None, timeout=None, **kw):
        self.calls.append((method, url, kw, headers, timeout))
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def client(responses, **kw):
    sleeps = []
    return GitHubClient("ghp_secret_token", session=Session(responses), sleep=sleeps.append, **kw), sleeps


def test_file_listing_is_paginated():
    c, _ = client([R(payload=[{"filename": f"f{i}"} for i in range(100)]),
                   R(payload=[{"filename": f"g{i}"} for i in range(100)]),
                   R(payload=[{"filename": "last"}])])
    files, truncated = c.list_pr_files("me", "repo", 1)
    assert len(files) == 201 and truncated is False
    pages = [call[2]["params"]["page"] for call in c.http.calls]
    assert pages == [1, 2, 3] and c.http.calls[0][2]["params"]["per_page"] == 100


def test_listing_reports_truncation_at_github_cap():
    c, _ = client([R(payload=[{}] * 100)] * 30)
    files, truncated = c.list_pr_files("me", "repo", 1)
    assert len(files) == 3000 and truncated is True


def test_rate_limit_is_waited_out_and_retried_once():
    c, sleeps = client([R(403, headers={"X-RateLimit-Remaining": "0", "Retry-After": "7"}), R(payload={"ok": 1})])
    assert c.get_pr("me", "repo", 1) == {"ok": 1} and sleeps == [7]


def test_server_errors_retry_a_bounded_number_of_times():
    c, sleeps = client([R(502), R(502), R(502)], max_retries=2)
    with pytest.raises(GitHubError) as err:
        c.get_pr("me", "repo", 1)
    assert err.value.status == 502 and len(c.http.calls) == 3 and sleeps == [1, 2]


def test_connection_errors_are_wrapped_without_leaking_the_token():
    c, _ = client([requests.ConnectionError("boom ghp_secret_token")] * 3, max_retries=2)
    with pytest.raises(GitHubError) as err:
        c.get_pr("me", "repo", 1)
    assert "ghp_secret_token" not in str(err.value)


def test_review_is_always_a_comment_never_approve():
    c, _ = client([R(payload={})])
    c.create_review("me", "repo", 1, "sha", "body", [{"path": "a.py", "line": 1, "side": "RIGHT", "body": "x"}])
    payload = c.http.calls[0][2]["json"]
    assert payload["event"] == "COMMENT" and payload["commit_id"] == "sha"
    assert c.http.calls[0][4] == (5, 30)                    # timeouts always set


def test_missing_token_is_a_clear_error():
    with pytest.raises(GitHubError):
        GitHubClient("")


# ---------------------------------------------------------------------- state
def test_claim_prevents_duplicates_and_allows_new_commits():
    s = ReviewStore(":memory:")
    assert s.claim("me/repo", 1, "sha1") is True
    assert s.claim("me/repo", 1, "sha1") is False           # in progress
    s.finish("me/repo", 1, "sha1", "completed", ["m"])
    assert s.claim("me/repo", 1, "sha1") is False           # done
    assert s.claim("me/repo", 1, "sha2") is True            # new commit
    assert s.claim("me/repo", 1, "sha1", force=True) is True


def test_failed_reviews_are_retried_but_only_a_bounded_number_of_times():
    s = ReviewStore(":memory:")
    s.claim("r/r", 1, "s")
    for _ in range(MAX_ATTEMPTS - 1):
        s.finish("r/r", 1, "s", "failed", error="x")
        assert s.claim("r/r", 1, "s") is True
    s.finish("r/r", 1, "s", "failed", error="x")
    assert s.claim("r/r", 1, "s") is False


def test_stale_running_review_is_recovered(monkeypatch):
    import app.state as state
    s = ReviewStore(":memory:")
    s.claim("r/r", 1, "s")
    real = state.time.time
    monkeypatch.setattr(state.time, "time", lambda: real() + STALE_RUNNING_SECONDS + 5)
    assert s.claim("r/r", 1, "s") is True


def test_file_backed_store_survives_restart(tmp_path):
    path = str(tmp_path / "sub" / "state.db")
    ReviewStore(path).claim("r/r", 1, "s")
    assert ReviewStore(path).claim("r/r", 1, "s") is False


# ------------------------------------------------------------ email + publish
def ctx():
    return PRContext("me/repo", 7, "Add <b>feature</b>", "https://github.com/me/repo/pull/7",
                    "me", "feature", "main", "a" * 40)


def finding(sev="High", line=3, title="Division by zero", file="app/main.py"):
    return ReviewFinding(category="bug", severity=sev, description="divisor may be zero",
                         recommendation="validate it", line=line, filename=file, confidence="High",
                         title=title, why_it_matters="crash")


def result(findings=None):
    r = ReviewResult(ctx(), "completed", findings=findings if findings is not None else [finding()],
                     models_used=["qwen2.5-coder:7b"], reviewed_files=1,
                     skipped_files=[("logo.png", "unsupported file type")], limitations=["1 note"])
    r.finish_now()
    return r


def test_report_email_has_html_text_and_required_fields():
    subject, body, text = build_report_email(result([finding("Critical"), finding("Low", 5, "Nit")]))
    for needed in ["me/repo", "#7", "pull/7", "feature", "main", "a" * 40, "qwen2.5-coder:7b",
                   "app/main.py:3", "validate it", "logo.png", "UTC"]:
        assert needed in body and needed in text
    assert "Critical" in body and "Low" in body and "[AI Review]" in subject


def test_email_html_escapes_untrusted_content():
    evil = finding(title="<script>alert(1)</script>")
    evil.recommendation = "<img src=x onerror=alert(1)>"
    _, body, _ = build_report_email(result([evil]))
    assert "<script>" not in body and "<img" not in body
    assert html.escape("<script>alert(1)</script>") in body
    assert "<b>feature</b>" not in body                      # PR title escaped too


def test_failure_email():
    subject, body, text = build_failure_email(ctx(), "All local Ollama models failed", "detail <x>")
    assert "FAILED" in subject and "&lt;x&gt;" in body and "No review was produced" in text


def test_notifier_catches_and_redacts_resend_errors():
    def boom(payload):
        raise RuntimeError("401 key re_testkey123 invalid")
    ok, err = EmailNotifier(make_settings(), sender=boom).send("s", "<p>h</p>", "t")
    assert ok is False and "re_testkey123" not in err and "RuntimeError" in err


def test_notifier_requires_configuration_and_sends_both_parts():
    assert EmailNotifier(make_settings(resend_api_key="")).send("s", "h", "t")[0] is False
    sent = []
    ok, _ = EmailNotifier(make_settings(), sender=sent.append).send("s", "<p>h</p>", "plain")
    assert ok and sent[0]["html"] == "<p>h</p>" and sent[0]["text"] == "plain" and sent[0]["to"] == ["me@example.com"]


def test_publish_attaches_inline_comments_only_to_diff_lines():
    gh = FakeGitHub()
    r = result([finding(line=3), finding(line=99, title="Elsewhere")])
    assert publish_review(gh, r, {"app/main.py": {1, 2, 3, 4}}, 25) == "published"
    review = gh.created[0]
    assert [c["line"] for c in review["comments"]] == [3]
    assert all(c["side"] == "RIGHT" for c in review["comments"])
    assert "Elsewhere" in review["body"] and marker("a" * 40) in review["body"]


def test_publish_is_idempotent_per_commit():
    gh = FakeGitHub()
    publish_review(gh, result(), {"app/main.py": {3}}, 25)
    assert publish_review(gh, result(), {"app/main.py": {3}}, 25) == "already-published"
    assert len(gh.created) == 1


def test_inline_comment_cap_moves_extras_to_the_summary():
    gh = FakeGitHub()
    many = [finding(line=i, title=f"T{i}") for i in range(1, 6)]
    publish_review(gh, result(many), {"app/main.py": set(range(1, 6))}, 2)
    assert len(gh.created[0]["comments"]) == 2 and "T5" in gh.created[0]["body"]


def test_invalid_inline_comments_fall_back_to_a_summary_review():
    gh = FakeGitHub()
    gh.create_errors = [GitHubError("422", 422)]
    publish_review(gh, result(), {"app/main.py": {3}}, 25)
    assert gh.created[0]["comments"] == [] and "Division by zero" in gh.created[0]["body"]
