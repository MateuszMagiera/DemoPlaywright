"""Progress Bar page object — https://demoqa.com/progress-bar."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class ProgressBarPage(BasePage):
    """Page object for the DemoQA Progress Bar widget page."""

    URL = "https://demoqa.com/progress-bar"

    # ── Locators ──────────────────────────────────────────────────────────────
    _START_STOP_BUTTON = "#startStopButton"
    _RESET_BUTTON = "#resetButton"
    _PROGRESS_BAR = "#progressBar .progress-bar"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the progress bar."""
        self.click(self._START_STOP_BUTTON)

    def stop(self) -> None:
        """Stop the progress bar."""
        self.click(self._START_STOP_BUTTON)

    def reset(self) -> None:
        """Reset the progress bar to 0%."""
        self.click(self._RESET_BUTTON)

    def wait_until_complete(self, *, timeout: float = 15_000) -> None:
        """Wait until progress reaches 100%."""
        self.page.wait_for_function(
            "document.querySelector('#progressBar .progress-bar').getAttribute('aria-valuenow') === '100'",
            timeout=timeout,
        )

    # ── Readers ───────────────────────────────────────────────────────────────

    def get_value(self) -> int:
        """Return the current progress bar value (0–100)."""
        val = self.page.locator(self._PROGRESS_BAR).get_attribute("aria-valuenow") or "0"
        return int(val)

    def is_reset_visible(self) -> bool:
        """Return True if the Reset button is visible (shown at 100%)."""
        return self.is_visible(self._RESET_BUTTON)
