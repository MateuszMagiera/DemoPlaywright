"""Backward-compatible re-export for the central logging configuration."""

from src.logging_config import get_logger, log_api_event, log_test_event

__all__ = ["get_logger", "log_api_event", "log_test_event"]
