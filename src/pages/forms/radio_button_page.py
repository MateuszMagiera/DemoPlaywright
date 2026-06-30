"""Radio Button page object — https://demoqa.com/radio-button."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class RadioButtonPage(BasePage):
    """Page object for the DemoQA Radio Button page."""

    URL = "https://demoqa.com/radio-button"

    # ── Locators ──────────────────────────────────────────────────────────────
    _YES_RADIO = "label[for='yesRadio']"
    _IMPRESSIVE_RADIO = "label[for='impressiveRadio']"
    _NO_RADIO = "label[for='noRadio']"
    _RESULT_TEXT = ".mt-3"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def select_yes(self) -> None:
        """Click the 'Yes' radio button."""
        self.click(self._YES_RADIO)

    def select_impressive(self) -> None:
        """Click the 'Impressive' radio button."""
        self.click(self._IMPRESSIVE_RADIO)

    def select_no(self) -> None:
        """Click the 'No' radio button (disabled on the page)."""
        self.click(self._NO_RADIO)

    # ── Readers ───────────────────────────────────────────────────────────────

    def get_selected_text(self) -> str:
        """Return the confirmation text shown after selection.

        Example: "You have selected Yes"
        """
        locator = self.page.locator(self._RESULT_TEXT)
        if not locator.is_visible():
            return ""
        return locator.inner_text().strip()

    def is_no_radio_disabled(self) -> bool:
        """Return True if the 'No' radio input is disabled."""
        return not self.page.locator("#noRadio").is_enabled()
