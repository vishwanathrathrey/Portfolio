"""Centralised configuration. Every setting comes from environment variables
(optionally loaded from a local .env file); nothing is hardcoded in code."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from dotenv import load_dotenv


def _int(env: Mapping[str, str], name: str, default: int) -> int:
    try:
        return int(env.get(name, default))
    except (TypeError, ValueError):
        return default


def _float(env: Mapping[str, str], name: str, default: float) -> float:
    try:
        return float(env.get(name, default))
    except (TypeError, ValueError):
        return default


def _bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    value = env.get(name)
    if value is None or value == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    # GitHub
    github_token: str = ""
    github_api_url: str = "https://api.github.com"
    webhook_secret: str = ""
    allowed_repos: tuple = ()
    publish_github_review: bool = True
    max_inline_comments: int = 25
    # Local Ollama (the only AI inference path)
    ollama_base_url: str = "http://localhost:11434"
    primary_model: str = "qwen2.5-coder:7b"
    fallback_model: str = "mistral"
    embedding_model: str = "nomic-embed-text"  # reserved; never used for generation
    connect_timeout: float = 5.0
    generate_timeout: float = 600.0
    max_retries: int = 1
    retry_backoff: float = 2.0
    num_ctx: int = 8192
    temperature: float = 0.1
    # Diff handling limits
    max_chunk_chars: int = 6000
    max_files: int = 50
    max_total_chars: int = 120000
    # Email (Resend)
    resend_api_key: str = ""
    email_to: str = ""
    email_from: str = "aireviewer@resend.dev"
    # Runtime
    state_db: str = ""
    app_env: str = "development"
    log_level: str = "INFO"


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    if env is None:
        load_dotenv()
        env = os.environ
    state_db = env.get("AI_REVIEW_STATE_DB") or str(
        Path.home() / ".ai-code-review" / "state.db"
    )
    repos = tuple(r.strip() for r in env.get("ALLOWED_REPOS", "").split(",") if r.strip())
    d = Settings()
    return Settings(
        github_token=env.get("GITHUB_TOKEN", ""),
        github_api_url=env.get("GITHUB_API_URL", d.github_api_url).rstrip("/"),
        webhook_secret=env.get("GITHUB_WEBHOOK_SECRET", ""),
        allowed_repos=repos,
        publish_github_review=_bool(env, "PUBLISH_GITHUB_REVIEW", d.publish_github_review),
        max_inline_comments=_int(env, "MAX_INLINE_COMMENTS", d.max_inline_comments),
        ollama_base_url=env.get("OLLAMA_BASE_URL", d.ollama_base_url).rstrip("/"),
        primary_model=env.get("OLLAMA_PRIMARY_MODEL", d.primary_model),
        fallback_model=env.get("OLLAMA_FALLBACK_MODEL", d.fallback_model),
        embedding_model=env.get("OLLAMA_EMBEDDING_MODEL", d.embedding_model),
        connect_timeout=_float(env, "OLLAMA_CONNECT_TIMEOUT", d.connect_timeout),
        generate_timeout=_float(env, "OLLAMA_GENERATE_TIMEOUT", d.generate_timeout),
        max_retries=max(0, _int(env, "OLLAMA_MAX_RETRIES", d.max_retries)),
        retry_backoff=_float(env, "OLLAMA_RETRY_BACKOFF", d.retry_backoff),
        num_ctx=_int(env, "OLLAMA_NUM_CTX", d.num_ctx),
        temperature=_float(env, "OLLAMA_TEMPERATURE", d.temperature),
        max_chunk_chars=_int(env, "MAX_CHUNK_CHARS", d.max_chunk_chars),
        max_files=_int(env, "MAX_FILES", d.max_files),
        max_total_chars=_int(env, "MAX_TOTAL_CHARS", d.max_total_chars),
        resend_api_key=env.get("RESEND_API_KEY", ""),
        email_to=env.get("REVIEW_EMAIL_TO", ""),
        email_from=env.get("REVIEW_EMAIL_FROM", d.email_from),
        state_db=state_db,
        app_env=env.get("APP_ENV", d.app_env),
        log_level=env.get("LOG_LEVEL", d.log_level).upper(),
    )
