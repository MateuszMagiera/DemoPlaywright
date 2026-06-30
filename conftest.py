"""Root conftest.py — shared Playwright fixtures for the entire test suite."""

from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.config import Settings, get_settings

# ──────────────────────────────────────────────────────────────────────────────
# Settings fixture
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Return project settings (cached singleton)."""
    return get_settings()


# ──────────────────────────────────────────────────────────────────────────────
# Playwright core fixtures
# ──────────────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Session-scoped Playwright instance."""
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, settings: Settings) -> Generator[Browser, None, None]:
    """Session-scoped browser — launched once, shared across all tests."""
    browser_type = getattr(playwright_instance, settings.browser)
    browser = browser_type.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo,
    )
    yield browser
    browser.close()


@pytest.fixture
def context(
    browser: Browser, settings: Settings, tmp_path: Path
) -> Generator[BrowserContext, None, None]:
    """Function-scoped browser context — isolated state per test."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        record_video_dir=str(tmp_path / "videos") if settings.video != "off" else None,
    )
    context.set_default_timeout(settings.default_timeout)
    context.set_default_navigation_timeout(settings.navigation_timeout)

    if settings.tracing != "off":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # ── teardown ──────────────────────────────────────────────────────────────
    _stop_tracing(context, settings)
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Function-scoped page — one page per test with auto-screenshot on failure."""
    page = context.new_page()
    yield page
    page.close()


# ──────────────────────────────────────────────────────────────────────────────
# Auto-screenshot on failure
# ──────────────────────────────────────────────────────────────────────────────


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):  # type: ignore[override]
    """Capture screenshot on test failure and attach to HTML / Allure report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        _capture_failure_screenshot(item)


def _capture_failure_screenshot(item: pytest.Item) -> None:
    """Save screenshot and attach to available reports."""
    page: Page | None = item.funcargs.get("page")  # type: ignore[assignment]
    if page is None:
        return

    screenshots_dir = Path("reports/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    safe_name = item.nodeid.replace("/", "_").replace("::", "__").replace(" ", "_")
    screenshot_path = screenshots_dir / f"{safe_name}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)

    # Attach to pytest-html
    try:
        extras = item.funcargs.get("extra")  # provided by pytest-html plugin
        if extras is not None:
            from pytest_html import extras as html_extras  # type: ignore[import]

            extras.append(html_extras.image(str(screenshot_path)))
    except Exception:
        pass

    # Attach to Allure
    try:
        import allure

        allure.attach.file(
            str(screenshot_path),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def _stop_tracing(context: BrowserContext, settings: Settings) -> None:
    """Save trace if tracing is enabled."""
    if settings.tracing == "off":
        return
    traces_dir = Path("reports/traces")
    traces_dir.mkdir(parents=True, exist_ok=True)
    trace_path = traces_dir / "trace.zip"
    context.tracing.stop(path=str(trace_path))
