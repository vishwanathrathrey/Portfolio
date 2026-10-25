import logging
import os

from pythonjsonlogger.json import JsonFormatter
from rich.logging import RichHandler

from app.config import settings


def configure_logging() -> None:
    """Configure Rich development logs or JSON logs when explicitly requested."""
    if os.getenv("LOG_FORMAT", "").lower() == "json":
        handler: logging.Handler = logging.StreamHandler()
        handler.setFormatter(
            JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
    else:
        handler = RichHandler(
            markup=True,
            rich_tracebacks=True,
            show_path=False,
            log_time_format="[%Y-%m-%d %H:%M:%S]",
        )
        handler.setFormatter(logging.Formatter("%(name)s | %(levelname)s | %(message)s"))
    logging.basicConfig(
        level=settings.log_level.upper(),
        handlers=[handler],
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """Return a named standard-library logger."""
    return logging.getLogger(name)
