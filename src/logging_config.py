"""Central logging configuration for tests and API/UI components."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
SESSION_LOG_PATH = LOG_DIR / f"test-session-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.jsonl"


class JsonLineFormatter(logging.Formatter):
    """Format log records as compact JSON lines for file output."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger instance."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(SESSION_LOG_PATH, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JsonLineFormatter())
    logger.addHandler(file_handler)

    return logger


def log_test_event(
    logger: logging.Logger, test_name: str, status: str, duration_ms: int | None = None
) -> None:
    """Log a simple test lifecycle event."""
    message = f"test_name={test_name} status={status}"
    if duration_ms is not None:
        message = f"{message} duration_ms={duration_ms}"
    logger.info("test_event | %s", message)


def log_api_event(
    logger: logging.Logger, method: str, url: str, status_code: int | None = None
) -> None:
    """Log a simple API request/response summary."""
    message = f"method={method} url={url}"
    if status_code is not None:
        message = f"{message} status_code={status_code}"
    logger.info("api_event | %s", message)
