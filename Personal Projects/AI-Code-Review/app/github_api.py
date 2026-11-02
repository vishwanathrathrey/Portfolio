"""GitHub REST client: pagination, timeouts, bounded retries, rate-limit aware.
The token is only ever sent in the Authorization header and never logged."""
from __future__ import annotations

import logging
import time

import requests

log = logging.getLogger(__name__)

PER_PAGE = 100
MAX_PAGES = 30          # GitHub caps "list PR files" at 3000 files
MAX_RATE_LIMIT_WAIT = 60


class GitHubError(Exception):
    def __init__(self, message, status=None):
        super().__init__(message)
        self.status = status


class GitHubClient:
    def __init__(self, token, base_url="https://api.github.com", session=None,
                 timeout=(5, 30), max_retries=2, sleep=time.sleep):
        if not token:
            raise GitHubError("GITHUB_TOKEN is not set")
        self.base_url = base_url.rstrip("/")
        self.http = session or requests.Session()
        self.timeout = timeout
        self.max_retries = max_retries
        self.sleep = sleep
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        for attempt in range(self.max_retries + 1):
            last = attempt == self.max_retries
            try:
                resp = self.http.request(method, url, headers=self._headers,
                                         timeout=self.timeout, **kwargs)
            except (requests.ConnectionError, requests.Timeout) as exc:
                if last:
                    raise GitHubError(f"GitHub unreachable: {type(exc).__name__}") from exc
                self.sleep(2 ** attempt)
                continue
            status = resp.status_code
            rate_limited = status == 429 or (
                status == 403 and resp.headers.get("X-RateLimit-Remaining") == "0")
            if rate_limited and not last:
                wait = min(int(resp.headers.get("Retry-After", 5) or 5), MAX_RATE_LIMIT_WAIT)
                log.warning("GitHub rate limit hit; waiting %ss", wait)
                self.sleep(wait)
                continue
            if status >= 500 and not last:
                self.sleep(2 ** attempt)
                continue
            if status >= 400:
                raise GitHubError(f"GitHub {method} {path} failed with HTTP {status}", status)
            return resp
        raise GitHubError("GitHub request failed")  # pragma: no cover

    def get_pr(self, owner, repo, number):
        return self._request("GET", f"/repos/{owner}/{repo}/pulls/{number}").json()

    def _paginate(self, path):
        items, truncated = [], False
        for page in range(1, MAX_PAGES + 1):
            batch = self._request("GET", path, params={"per_page": PER_PAGE, "page": page}).json()
            items.extend(batch)
            if len(batch) < PER_PAGE:
                return items, False
        return items, True

    def list_pr_files(self, owner, repo, number):
        """All changed files (paginated). Returns (files, truncated)."""
        return self._paginate(f"/repos/{owner}/{repo}/pulls/{number}/files")

    def list_reviews(self, owner, repo, number):
        return self._paginate(f"/repos/{owner}/{repo}/pulls/{number}/reviews")[0]

    def create_review(self, owner, repo, number, commit_id, body, comments):
        """Post a COMMENT review (never APPROVE / REQUEST_CHANGES)."""
        payload = {"commit_id": commit_id, "body": body, "event": "COMMENT"}
        if comments:
            payload["comments"] = comments
        return self._request("POST", f"/repos/{owner}/{repo}/pulls/{number}/reviews",
                             json=payload).json()
