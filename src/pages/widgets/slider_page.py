"""Slider page object — https://demoqa.com/slider."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class SliderPage(BasePage):
    """Page object for the DemoQA Slider widget page."""

    URL = "https://demoqa.com/slider"

    # ── Locators ──────────────────────────────────────────────────────────────
    _SLIDER_INPUT = "input[type='range']"
    _SLIDER_VALUE = "#sliderValue"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def set_value(self, value: int) -> None:
        """Set the slider to *value* by manipulating the input element directly."""
        self.page.locator(self._SLIDER_INPUT).fill(str(value))
        # Dispatch input + change events so the page reacts
        self.page.locator(self._SLIDER_INPUT).dispatch_event("input")
        self.page.locator(self._SLIDER_INPUT).dispatch_event("change")

    # ── Readers ───────────────────────────────────────────────────────────────

    def get_current_value(self) -> int:
        """Return the currently displayed slider value as an integer."""
        return int(self.page.locator(self._SLIDER_VALUE).input_value())

    def get_min(self) -> int:
        """Return the slider's minimum value."""
        return int(self.page.locator(self._SLIDER_INPUT).get_attribute("min") or "0")

    def get_max(self) -> int:
        """Return the slider's maximum value."""
        return int(self.page.locator(self._SLIDER_INPUT).get_attribute("max") or "100")
