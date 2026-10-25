from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ollama_base_url: str = "http://localhost:11434"
    model_planner: str = "qwen2.5-coder:3b"
    model_writer: str = "mistral:latest"
    model_reflector: str = "mistral:latest"
    output_dir: Path = Path("./output")
    log_level: str = "INFO"
    max_request_len: int = 4000
    llm_timeout_seconds: int = 120
    llm_max_retries: int = 2


settings = Settings()


def ensure_output_dir() -> Path:
    """Create the configured output directory when it does not exist."""
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    return settings.output_dir
