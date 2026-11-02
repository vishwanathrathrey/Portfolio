"""Optional webhook receiver. The primary trigger is the GitHub Actions workflow
(.github/workflows/ai-code-review.yml); use this only if you prefer GitHub webhooks
and can expose this port through a secured tunnel.

It authenticates every delivery with the webhook secret, acknowledges immediately
(GitHub times out after 10 s) and runs reviews one at a time in a background worker,
sharing the same pipeline and duplicate-prevention store as the CLI."""
from __future__ import annotations

import hashlib
import hmac
import logging
import os
import threading
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request

from app.config import load_settings
from app.logging_utils import setup_logging

HANDLED_ACTIONS = {"opened", "synchronize", "reopened", "ready_for_review"}
MAX_SEEN_DELIVERIES = 1000

log = logging.getLogger("webhook")
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

_executor = ThreadPoolExecutor(max_workers=1)   # one Ollama job at a time
_seen = OrderedDict()
_seen_lock = threading.Lock()
_pipeline = None


def is_valid_signature(raw_body: bytes, signature_header, secret: str) -> bool:
    """Verify GitHub's X-Hub-Signature-256 header. A missing secret never validates."""
    if not secret or not signature_header:
        return False
    expected = "sha256=" + hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_header)


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        from run_review import build_pipeline
        _pipeline = build_pipeline(load_settings())
    return _pipeline


def _run_review(repo, number):
    try:
        result = _get_pipeline().run(repo, number)
        log.info("%s#%s -> %s", repo, number, result.status)
    except Exception:
        log.exception("review job crashed for %s#%s", repo, number)


def _already_seen(delivery_id) -> bool:
    if not delivery_id:
        return False
    with _seen_lock:
        if delivery_id in _seen:
            return True
        _seen[delivery_id] = True
        while len(_seen) > MAX_SEEN_DELIVERIES:
            _seen.popitem(last=False)
    return False


@app.route("/")
def home():
    return {"service": "ai-code-review-webhook", "status": "running"}


@app.route("/webhook", methods=["POST"])
def webhook():
    settings = load_settings()
    if not settings.webhook_secret:
        return {"status": "GITHUB_WEBHOOK_SECRET is not configured"}, 503
    if not is_valid_signature(request.get_data(), request.headers.get("X-Hub-Signature-256"),
                              settings.webhook_secret):
        return {"status": "invalid signature"}, 401

    event = request.headers.get("X-GitHub-Event")
    if event == "ping":
        return {"status": "pong"}, 200
    payload = request.get_json(silent=True)
    if event != "pull_request" or not isinstance(payload, dict):
        return {"status": "ignored"}, 200
    if payload.get("action") not in HANDLED_ACTIONS:
        return {"status": "ignored"}, 200

    try:
        repo = payload["repository"]["full_name"]
        number = int(payload["pull_request"]["number"])
    except (KeyError, TypeError, ValueError):
        return {"status": "invalid payload"}, 400

    if _already_seen(request.headers.get("X-GitHub-Delivery")):
        return {"status": "duplicate delivery"}, 200

    _executor.submit(_run_review, repo, number)
    return {"status": "accepted"}, 202


if __name__ == "__main__":
    cfg = load_settings()
    setup_logging(cfg)
    # The Werkzeug debugger allows remote code execution: debug is opt-in only.
    app.run(host=os.getenv("WEBHOOK_HOST", "127.0.0.1"),
            port=int(os.getenv("WEBHOOK_PORT", "5000")),
            debug=os.getenv("FLASK_DEBUG") == "1")
