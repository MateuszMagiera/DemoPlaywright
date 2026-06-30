"""Alerts page object — https://demoqa.com/alerts."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class AlertsPage(BasePage):
    """Page object for the DemoQA Alerts page."""

    URL = "https://demoqa.com/alerts"

    # ── Locators ──────────────────────────────────────────────────────────────
    _SIMPLE_ALERT_BTN = "#alertButton"
    _TIMER_ALERT_BTN = "#timerAlertButton"
    _CONFIRM_BTN = "#confirmButton"
    _PROMPT_BTN = "#promtButton"
    _CONFIRM_RESULT = "#confirmResult"
    PROMPT_RESULT = "#promptResult"  # public: used in tests to check visibility

    # Keep private alias for backward compat
    _PROMPT_RESULT = PROMPT_RESULT

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Alert actions ─────────────────────────────────────────────────────────

    def click_simple_alert(self) -> None:
        """Trigger the simple 'Click me' alert."""
        self.click(self._SIMPLE_ALERT_BTN)

    def click_timer_alert(self) -> None:
        """Trigger the timer-based alert (appears after ~5 s)."""
        self.click(self._TIMER_ALERT_BTN)

    def accept_dialog(self) -> None:
        """Register a one-time handler that accepts the next dialog."""
        self.page.once("dialog", lambda d: d.accept())

    def dismiss_dialog(self) -> None:
        """Register a one-time handler that dismisses the next dialog."""
        self.page.once("dialog", lambda d: d.dismiss())

    def accept_dialog_with_text(self, text: str) -> None:
        """Register a one-time handler that accepts and fills *text* into a prompt."""
        self.page.once("dialog", lambda d: d.accept(text))

    # ── Confirm dialog ────────────────────────────────────────────────────────

    def click_confirm(self) -> None:
        """Trigger the Confirm dialog."""
        self.click(self._CONFIRM_BTN)

    def get_confirm_result(self) -> str:
        """Return the text displayed after confirm/dismiss."""
        return self.get_text(self._CONFIRM_RESULT)

    # ── Prompt dialog ─────────────────────────────────────────────────────────

    def click_prompt(self) -> None:
        """Trigger the Prompt dialog."""
        self.click(self._PROMPT_BTN)

    def get_prompt_result(self) -> str:
        """Return the text displayed after prompt is answered."""
        return self.get_text(self._PROMPT_RESULT)
