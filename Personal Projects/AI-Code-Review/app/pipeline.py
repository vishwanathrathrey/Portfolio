"""End-to-end PR review: fetch -> filter -> chunk -> review (local Ollama) ->
validate -> publish to GitHub -> e-mail. One entry point shared by the GitHub
Action CLI and the optional webhook server."""
from __future__ import annotations

import logging
import re

from app.diff_utils import added_lines, chunk_patch, commentable_lines, skip_reason
from app.github_api import GitHubError
from app.github_publisher import publish_review
from app.models import ReviewFinding
from app.notifier import build_failure_email, build_report_email
from app.providers import AllModelsFailed
from app.report_model import PRContext, ReviewResult, severity_rank
from app.review_schema import build_prompt, parse_review
from app.security_scanner import scan_added_lines
from app.user_registry import get_user_email

log = logging.getLogger(__name__)
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class ReviewPipeline:
    def __init__(self, settings, github, router, store, notifier):
        self.s = settings
        self.github = github
        self.router = router
        self.store = store
        self.notifier = notifier

    # ------------------------------------------------------------------ entry
    def run(self, repo: str, number: int, force: bool = False) -> ReviewResult:
        ctx = PRContext(repo, number, "", f"https://github.com/{repo}/pull/{number}", "", "", "", "")
        if not REPO_RE.match(repo) or not isinstance(number, int) or number < 1:
            return ReviewResult(ctx, "skipped", notes=["invalid repository or PR number"])
        if self.s.allowed_repos and repo not in self.s.allowed_repos:
            return ReviewResult(ctx, "skipped", notes=[f"{repo} is not in ALLOWED_REPOS"])

        try:
            pr = self.github.get_pr(ctx.owner, ctx.name, number)
        except GitHubError as exc:
            return self._fail_early(ctx, "GitHub API error", str(exc))

        ctx = PRContext(
            repo, number, pr.get("title", ""), pr.get("html_url", ctx.url),
            (pr.get("user") or {}).get("login", ""), pr["head"]["ref"], pr["base"]["ref"],
            pr["head"]["sha"])

        skip = self._skip_reason(pr)
        if skip:
            log.info("skipping %s#%s: %s", repo, number, skip)
            return ReviewResult(ctx, "skipped", notes=[skip])

        if not self.store.claim(repo, number, ctx.head_sha, force):
            return self._resume_or_duplicate(ctx)

        try:
            result, commentable = self._review(ctx)
        except AllModelsFailed as exc:
            return self._fail(ctx, "All local Ollama models failed", str(exc))
        except GitHubError as exc:
            return self._fail(ctx, "GitHub API error", str(exc))
        except Exception as exc:  # last-resort guard: never report a silent success
            log.exception("unexpected failure reviewing %s#%s", repo, number)
            return self._fail(ctx, "Unexpected processing error", f"{type(exc).__name__}: {exc}")

        result.status = "completed"
        result.finish_now()
        self.store.finish(repo, number, ctx.head_sha, "completed", result.models_used,
                          report_json=result.to_json())
        self._deliver(result, commentable)
        return result

    # ------------------------------------------------------------- guard rails
    @staticmethod
    def _skip_reason(pr):
        if pr.get("state") != "open":
            return "PR is not open"
        if pr.get("draft"):
            return "PR is a draft (reviewed when marked ready for review)"
        head_repo = (pr["head"].get("repo") or {}).get("full_name")
        base_repo = (pr["base"].get("repo") or {}).get("full_name")
        if not head_repo or head_repo != base_repo:
            return "PR comes from a fork or deleted repository; fork PRs are never reviewed"
        return None

    def _resume_or_duplicate(self, ctx):
        row = self.store.get(ctx.repo, ctx.number, ctx.head_sha)
        if row and row["status"] == "completed" and not row["emailed"] and row["report_json"]:
            log.info("review already complete; retrying undelivered e-mail")
            result = ReviewResult.from_json(row["report_json"])
            self._deliver(result, {}, publish=False)
            return result
        log.info("duplicate: %s#%s @ %s already handled", ctx.repo, ctx.number, ctx.head_sha[:10])
        return ReviewResult(ctx, "duplicate", notes=["this commit was already reviewed or is in progress"])

    # ---------------------------------------------------------------- review
    def _review(self, ctx):
        result = ReviewResult(ctx, "running")
        files, truncated = self.github.list_pr_files(ctx.owner, ctx.name, ctx.number)
        if truncated:
            result.limitations.append("GitHub lists at most 3000 changed files; the remainder was not reviewed.")

        selected, total = [], 0
        for f in files:
            reason = skip_reason(f)
            if not reason and len(selected) >= self.s.max_files:
                reason = f"exceeds MAX_FILES limit ({self.s.max_files})"
            elif not reason and total + len(f["patch"]) > self.s.max_total_chars:
                reason = f"exceeds MAX_TOTAL_CHARS budget ({self.s.max_total_chars})"
            if reason:
                result.skipped_files.append((f["filename"], reason))
                continue
            total += len(f["patch"])
            selected.append(f)

        findings, models, rejected, dropped, truncated_lines = [], [], 0, 0, 0
        commentable = {}
        for f in selected:
            name, patch = f["filename"], f["patch"]
            commentable[name] = commentable_lines(patch)
            chunks = chunk_patch(name, patch, self.s.max_chunk_chars)
            if not chunks:
                result.skipped_files.append((name, "only removed lines; nothing to review"))
                continue
            result.reviewed_files += 1
            findings += scan_added_lines(added_lines(patch), name)
            for chunk in chunks:
                truncated_lines += chunk.truncated_lines
                gen = self.router.generate(build_prompt(name, chunk.text), parse_review)
                if gen.model not in models:
                    models.append(gen.model)
                dropped += gen.parsed.dropped
                for item in gen.parsed.items:
                    if item["line"] not in chunk.added:
                        rejected += 1
                        continue
                    findings.append(ReviewFinding(
                        category=item["category"], severity=item["severity"].title(),
                        description=item["explanation"], recommendation=item["suggestion"],
                        line=item["line"], filename=name, confidence=item["confidence"].title(),
                        title=item["title"], why_it_matters=item["why_it_matters"], source="ai"))

        if rejected:
            result.limitations.append(
                f"{rejected} model finding(s) were discarded because they did not reference an added line.")
        if dropped:
            result.limitations.append(f"{dropped} malformed model finding(s) were discarded.")
        if truncated_lines:
            result.limitations.append(f"{truncated_lines} very long line(s) were truncated in the prompt.")
        if not result.reviewed_files:
            result.limitations.append("No reviewable source changes were found in this PR.")

        result.findings = self._dedupe(findings)
        result.models_used = models
        return result, commentable

    @staticmethod
    def _dedupe(findings):
        """One finding per (file, line, category); keep the most severe."""
        best = {}
        for f in findings:
            key = (f.filename, f.line, f.category)
            if key not in best or severity_rank(f.severity) < severity_rank(best[key].severity):
                best[key] = f
        return sorted(best.values(), key=lambda f: (severity_rank(f.severity), f.filename, f.line))

    # -------------------------------------------------------------- delivery
    def _deliver(self, result, commentable, publish=True):
        ctx = result.ctx
        if publish:
            if not (self.s.publish_github_review and self.s.github_token):
                result.publish_status = "disabled"
            else:
                try:
                    result.publish_status = publish_review(
                        self.github, result, commentable, self.s.max_inline_comments)
                    self.store.mark(ctx.repo, ctx.number, ctx.head_sha, "published")
                except GitHubError as exc:
                    result.publish_status = "failed"
                    result.notes.append(f"GitHub review was not published: {exc}")
                    log.error("publishing failed: %s", exc)

        subject, html_body, text = build_report_email(result)
        recipient = self.s.email_to or get_user_email(ctx.author)
        ok, err = self.notifier.send(subject, html_body, text, to=recipient)
        result.email_delivered = ok
        if ok:
            self.store.mark(ctx.repo, ctx.number, ctx.head_sha, "emailed")
        else:
            result.notes.append(f"Email was not delivered: {err}")
            log.error("review e-mail not delivered: %s", err)

    # --------------------------------------------------------------- failure
    def _fail(self, ctx, reason, detail):
        log.error("review failed for %s#%s: %s - %s", ctx.repo, ctx.number, reason, detail)
        self.store.finish(ctx.repo, ctx.number, ctx.head_sha, "failed", error=f"{reason}: {detail}")
        result = ReviewResult(ctx, "failed", error=f"{reason}: {detail}")
        result.finish_now()
        row = self.store.get(ctx.repo, ctx.number, ctx.head_sha)
        if not (row and row["failure_notified"]):
            subject, html_body, text = build_failure_email(ctx, reason, detail)
            ok, err = self.notifier.send(subject, html_body, text,
                                         to=self.s.email_to or get_user_email(ctx.author))
            if ok:
                self.store.mark(ctx.repo, ctx.number, ctx.head_sha, "failure_notified")
            else:
                result.notes.append(f"Failure notification not delivered: {err}")
        return result

    def _fail_early(self, ctx, reason, detail):
        """Failure before the head SHA is known (cannot be tracked in the store)."""
        log.error("review failed for %s#%s: %s - %s", ctx.repo, ctx.number, reason, detail)
        result = ReviewResult(ctx, "failed", error=f"{reason}: {detail}")
        subject, html_body, text = build_failure_email(ctx, reason, detail)
        ok, err = self.notifier.send(subject, html_body, text, to=self.s.email_to)
        if not ok:
            result.notes.append(f"Failure notification not delivered: {err}")
        return result
