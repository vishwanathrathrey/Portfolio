"""Publish a review to the PR as a COMMENT review (never approve / request changes /
merge). Inline comments are only attached to lines that are part of the PR diff."""
from __future__ import annotations

import logging

from app.github_api import GitHubError
from app.report_model import SEVERITY_ORDER, severity_rank

log = logging.getLogger(__name__)

ICONS = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "⚪"}


def marker(sha: str) -> str:
    return f"<!-- ai-code-review sha={sha} -->"


def _finding_body(f) -> str:
    title = f.title or f.description
    lines = [f"{ICONS.get(f.severity.lower(), '')} **{f.severity}** · {f.category} · confidence {f.confidence}",
             f"**{title}**"]
    if f.title and f.description:
        lines.append(f.description)
    if f.why_it_matters:
        lines.append(f"_Why it matters:_ {f.why_it_matters}")
    lines.append(f"**Suggested fix:** {f.recommendation}")
    return "\n\n".join(lines)


def build_review_body(result, inline_count: int, overflow) -> str:
    ctx = result.ctx
    counts = {k: len(v) for k, v in result.by_severity().items()}
    summary = " · ".join(f"{ICONS[k]} {counts[k]} {k}" for k in SEVERITY_ORDER)
    parts = [marker(ctx.head_sha), "## 🤖 AI Code Review (local Ollama)",
             f"Commit `{ctx.head_sha[:10]}` · model(s): {', '.join(result.models_used) or 'n/a'} · "
             f"{result.reviewed_files} file(s) reviewed", summary or "No issues found."]
    if not result.findings:
        parts.append("No actionable issues were found in the reviewed changes.")
    if inline_count:
        parts.append(f"{inline_count} finding(s) are attached as inline comments.")
    if overflow:
        parts.append("**Additional findings (not shown inline):**")
        parts += [f"- `{f.filename}:{f.line}` **{f.severity}** {f.title or f.description}: {f.recommendation}"
                  for f in overflow]
    limits = list(result.limitations) + [f"Skipped `{n}`: {r}" for n, r in result.skipped_files]
    if limits:
        parts.append("**Review limitations:**\n" + "\n".join(f"- {x}" for x in limits))
    parts.append("_Automated, advisory review. It never approves or merges._")
    return "\n\n".join(parts)


def publish_review(client, result, commentable: dict, max_inline: int) -> str:
    """Returns 'published' or 'already-published'. Raises GitHubError on failure."""
    ctx = result.ctx
    tag = marker(ctx.head_sha)
    for review in client.list_reviews(ctx.owner, ctx.name, ctx.number):
        if tag in (review.get("body") or ""):
            return "already-published"

    ordered = sorted(result.findings, key=lambda f: (severity_rank(f.severity), f.filename, f.line))
    inline, overflow = [], []
    for f in ordered:
        if len(inline) < max_inline and f.line in commentable.get(f.filename, set()):
            inline.append(f)
        else:
            overflow.append(f)
    comments = [{"path": f.filename, "line": f.line, "side": "RIGHT", "body": _finding_body(f)}
                for f in inline]
    body = build_review_body(result, len(inline), overflow)
    try:
        client.create_review(ctx.owner, ctx.name, ctx.number, ctx.head_sha, body, comments)
    except GitHubError as exc:
        if exc.status != 422 or not comments:
            raise
        log.warning("inline comments rejected (HTTP 422); posting summary only")
        body = build_review_body(result, 0, ordered)
        client.create_review(ctx.owner, ctx.name, ctx.number, ctx.head_sha, body, [])
    return "published"
