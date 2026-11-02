"""Resend e-mail notifications (HTML + plain-text). All dynamic text is
HTML-escaped; delivery errors are caught, classified and returned, never raised."""
from __future__ import annotations

import html
import logging

from app.logging_utils import redact
from app.report_model import SEVERITY_ORDER

log = logging.getLogger(__name__)

COLORS = {"critical": "#b71c1c", "high": "#e65100", "medium": "#f9a825", "low": "#546e7a"}
LABELS = {"critical": "Critical", "high": "High", "medium": "Medium", "low": "Low"}


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def build_report_email(result):
    ctx = result.ctx
    groups = result.by_severity()
    counts = {k: len(v) for k, v in groups.items()}
    summary = ", ".join(f"{counts[k]} {LABELS[k].lower()}" for k in SEVERITY_ORDER) or "none"
    verdict = "no issues found" if not result.findings else f"{len(result.findings)} finding(s): {summary}"
    models = ", ".join(result.models_used) or "n/a"
    subject = f"[AI Review] {ctx.repo} #{ctx.number}: {verdict}"[:200]

    meta = [
        ("Repository", ctx.repo), ("Pull request", f"#{ctx.number} {ctx.title}"),
        ("URL", ctx.url), ("Author", ctx.author),
        ("Branches", f"{ctx.head_ref} -> {ctx.base_ref}"), ("Commit", ctx.head_sha),
        ("Completed", result.completed_at), ("Model(s)", models),
        ("Files reviewed", result.reviewed_files),
    ]
    h = [f"<h2>AI Code Review: {_e(verdict)}</h2>", '<table cellpadding="4" style="font-size:14px">']
    h += [f"<tr><td><b>{_e(k)}</b></td><td>{_e(v)}</td></tr>" for k, v in meta]
    h.append("</table>")
    t = [f"AI Code Review: {verdict}", ""] + [f"{k}: {v}" for k, v in meta] + [""]

    for sev in SEVERITY_ORDER:
        items = groups.get(sev, [])
        if not items:
            continue
        h.append(f'<h3 style="color:{COLORS[sev]}">{LABELS[sev]} ({len(items)})</h3>')
        t.append(f"== {LABELS[sev]} ({len(items)}) ==")
        for f in items:
            title = f.title or f.description
            h.append(
                f"<div style='margin:0 0 12px;padding:8px;border-left:4px solid {COLORS[sev]}'>"
                f"<b>{_e(title)}</b> <code>{_e(f.filename)}:{_e(f.line)}</code> "
                f"<i>({_e(f.category)}, confidence {_e(f.confidence)})</i><br>"
                f"{_e(f.description if f.title else '')}"
                f"{'<br><b>Why it matters:</b> ' + _e(f.why_it_matters) if f.why_it_matters else ''}"
                f"<br><b>Suggested fix:</b> {_e(f.recommendation)}</div>")
            t += [f"- {title} [{f.filename}:{f.line}] ({f.category}, {f.confidence})",
                  f"  Why: {f.why_it_matters}" if f.why_it_matters else "",
                  f"  Fix: {f.recommendation}"]

    limits = list(result.limitations) + [f"Skipped {n}: {r}" for n, r in result.skipped_files]
    if limits:
        h.append("<h3>Review limitations</h3><ul>" + "".join(f"<li>{_e(x)}</li>" for x in limits) + "</ul>")
        t += ["", "Review limitations:"] + [f"- {x}" for x in limits]
    if result.notes:
        h.append("<h3>Delivery notes</h3><ul>" + "".join(f"<li>{_e(x)}</li>" for x in result.notes) + "</ul>")
        t += ["", "Delivery notes:"] + [f"- {x}" for x in result.notes]
    return subject, "".join(h), "\n".join(x for x in t if x is not None)


def build_failure_email(ctx, reason: str, detail: str = ""):
    subject = f"[AI Review FAILED] {ctx.repo} #{ctx.number}: {reason}"[:200]
    meta = f"{ctx.repo} #{ctx.number} ({ctx.url}) commit {ctx.head_sha}"
    html_body = (f"<h2>AI Code Review failed</h2><p><b>{_e(reason)}</b></p>"
                 f"<p>{_e(meta)}</p><pre>{_e(detail)}</pre>"
                 "<p>No review was produced for this commit. Re-run the workflow to retry.</p>")
    text = f"AI Code Review FAILED\n{reason}\n{meta}\n\n{detail}\n\nNo review was produced for this commit."
    return subject, html_body, text


class EmailNotifier:
    def __init__(self, settings, sender=None):
        self.settings = settings
        self._sender = sender

    def _default_send(self, payload):
        import resend
        resend.api_key = self.settings.resend_api_key
        return resend.Emails.send(payload)

    def send(self, subject, html_body, text, to=None):
        """Returns (ok, error_message). Never raises."""
        recipient = to or self.settings.email_to
        if not self.settings.resend_api_key or not recipient:
            return False, "email not configured (RESEND_API_KEY / REVIEW_EMAIL_TO)"
        payload = {"from": self.settings.email_from, "to": [recipient],
                   "subject": subject, "html": html_body, "text": text}
        try:
            (self._sender or self._default_send)(payload)
            return True, ""
        except Exception as exc:  # Resend raises several error types
            message = redact(f"{type(exc).__name__}: {exc}", [self.settings.resend_api_key])
            log.error("email delivery failed: %s", message)
            return False, message
