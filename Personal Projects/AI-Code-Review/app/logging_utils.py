"""Logging setup with secret redaction (tokens must never reach logs)."""
from __future__ import annotations

import logging


def redact(text: str, secrets) -> str:
    for secret in secrets:
        if secret and len(secret) >= 6:
            text = text.replace(secret, "***")
    return text


class RedactingFilter(logging.Filter):
    def __init__(self, secrets):
        super().__init__()
        self._secrets = list(secrets)

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact(record.getMessage(), self._secrets)
        record.args = ()
        return True


def setup_logging(settings) -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    flt = RedactingFilter(
        [settings.github_token, settings.resend_api_key, settings.webhook_secret]
    )
    for handler in logging.getLogger().handlers:
        handler.addFilter(flt)
