"""Shared fakes: no real GitHub, Ollama or Resend is ever contacted in tests."""
import json

from app.config import Settings
from app.github_api import GitHubError
from app.providers import AllModelsFailed, GenerationResult
from app.state import ReviewStore

PATCH = (
    "@@ -1,3 +1,5 @@\n"
    " import os\n"
    "+API_KEY = 'abc123456'\n"
    "+value = 10 / divisor\n"
    " print(value)\n"
    "-old = 1\n"
)


def make_settings(**overrides):
    base = dict(github_token="ghp_testtoken123", resend_api_key="re_testkey123",
                email_to="me@example.com", state_db=":memory:", retry_backoff=0.0)
    base.update(overrides)
    return Settings(**base)


def make_pr(sha="a" * 40, state="open", draft=False, head_repo="me/repo", base_repo="me/repo"):
    return {
        "title": "Add feature", "html_url": "https://github.com/me/repo/pull/7", "state": state,
        "draft": draft, "user": {"login": "me"},
        "head": {"ref": "feature", "sha": sha, "repo": {"full_name": head_repo} if head_repo else None},
        "base": {"ref": "main", "repo": {"full_name": base_repo}},
    }


def finding_json(line=3, severity="high", title="Division by zero", category="bug"):
    return json.dumps({"findings": [{
        "title": title, "category": category, "severity": severity, "confidence": "high",
        "line": line, "explanation": "divisor may be zero", "why_it_matters": "crashes at runtime",
        "suggestion": "validate the divisor first"}]})


class FakeGitHub:
    def __init__(self, pr=None, files=None, reviews=None, truncated=False):
        self.pr = pr or make_pr()
        self.files = files if files is not None else [
            {"filename": "app/main.py", "status": "modified", "patch": PATCH}]
        self.reviews = reviews or []
        self.truncated = truncated
        self.created = []
        self.fail_pr = None
        self.fail_files = None
        self.create_errors = []

    def get_pr(self, owner, repo, number):
        if self.fail_pr:
            raise self.fail_pr
        return self.pr

    def list_pr_files(self, owner, repo, number):
        if self.fail_files:
            raise self.fail_files
        return self.files, self.truncated

    def list_reviews(self, owner, repo, number):
        return self.reviews + [{"body": c["body"]} for c in self.created]

    def create_review(self, owner, repo, number, commit_id, body, comments):
        if self.create_errors:
            raise self.create_errors.pop(0)
        self.created.append({"commit_id": commit_id, "body": body, "comments": comments})
        return {}


class FakeRouter:
    """Returns scripted raw model responses through the REAL output validator."""

    def __init__(self, responses=None, model="qwen2.5-coder:7b", fail=None):
        self.responses = list(responses or [])
        self.model = model
        self.fail = fail
        self.prompts = []

    def generate(self, prompt, parse):
        self.prompts.append(prompt)
        if self.fail:
            raise self.fail
        raw = self.responses.pop(0) if self.responses else '{"findings": []}'
        return GenerationResult(parse(raw), self.model)


class FakeNotifier:
    def __init__(self, ok=True):
        self.ok = ok
        self.sent = []

    def send(self, subject, html_body, text, to=None):
        self.sent.append({"subject": subject, "html": html_body, "text": text, "to": to})
        return (True, "") if self.ok else (False, "resend down")


def make_store():
    return ReviewStore(":memory:")


__all__ = ["AllModelsFailed", "GitHubError"]
