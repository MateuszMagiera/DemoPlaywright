"""Pytest plugin for structured test lifecycle logging and session summary."""

from __future__ import annotations

import time
from collections import Counter

import pytest

from src.logging_config import get_logger
from src.utils.github_summary import write_github_summary
from src.utils.notifier import SlackNotifier

logger = get_logger("pytest.plugin")
notifier = SlackNotifier()

_STATS: Counter[str] = Counter()
_SESSION_START: float | None = None


def pytest_configure(config: pytest.Config) -> None:
    """Initialize plugin state when pytest starts."""
    global _SESSION_START
    _SESSION_START = time.perf_counter()
    logger.info("pytest_session_start | rootdir=%s", config.rootpath)


def pytest_runtest_setup(item: pytest.Item) -> None:
    """Log test start before execution."""
    logger.info("pytest_setup | test_name=%s", item.nodeid)


def pytest_runtest_call(item: pytest.Item) -> None:
    """Log test call stage."""
    logger.info("pytest_call | test_name=%s", item.nodeid)


def pytest_runtest_logreport(report: pytest.CollectReport | pytest.TestReport) -> None:
    """Record and log each test report."""
    if not hasattr(report, "nodeid"):
        return

    if report.when == "call" and report.outcome in {"passed", "failed", "skipped"}:
        status = report.outcome
        duration_ms = int(report.duration * 1000)
        _STATS[status] += 1
        logger.info(
            "pytest_report | test_name=%s status=%s duration_ms=%s",
            report.nodeid,
            status,
            duration_ms,
        )
    elif report.when == "setup" and report.outcome == "skipped":
        _STATS["skipped"] += 1
        logger.info("pytest_report | test_name=%s status=skipped duration_ms=0", report.nodeid)


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Print a concise summary table when the session ends."""
    if _SESSION_START is None:
        duration = 0.0
    else:
        duration = time.perf_counter() - _SESSION_START

    passed = _STATS.get("passed", 0)
    failed = _STATS.get("failed", 0)
    skipped = _STATS.get("skipped", 0)

    logger.info(
        "pytest_session_finish | passed=%s failed=%s skipped=%s duration_s=%.2f exitstatus=%s",
        passed,
        failed,
        skipped,
        duration,
        exitstatus,
    )

    print()
    print("+--------------------------------------------+")
    print(f"| PASSED: {passed} | FAILED: {failed} | SKIPPED: {skipped} |")
    print(f"| Duration: {duration:.2f}s{' ' * 14}|")
    print("+--------------------------------------------+")

    notifier.send_summary(
        passed=passed,
        failed=failed,
        skipped=skipped,
        duration=duration,
    )

    write_github_summary(
        passed=passed,
        failed=failed,
        skipped=skipped,
        duration=duration,
    )
