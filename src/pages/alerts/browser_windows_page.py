"""Browser Windows page object — https://demoqa.com/browser-windows."""

from __future__ import annotations

from playwright.sync_api import BrowserContext, Page

from src.pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    """Page object for the DemoQA Browser Windows page."""

    URL = "https://demoqa.com/browser-windows"

    # ── Locators ──────────────────────────────────────────────────────────────
    _NEW_TAB_BTN = "#tabButton"
    _NEW_WINDOW_BTN = "#windowButton"
    _NEW_WINDOW_MSG_BTN = "#messageWindowButton"
    _SAMPLE_HEADING = "#sampleHeading"

    def __init__(self, page: Page, context: BrowserContext) -> None:
        super().__init__(page)
        self.context = context

    # ── Actions ───────────────────────────────────────────────────────────────

    def open_new_tab(self) -> Page:
        """Click 'New Tab' and return the new Page object."""
        with self.context.expect_page() as new_page_info:
            self.click(self._NEW_TAB_BTN)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    def open_new_window(self) -> Page:
        """Click 'New Window' and return the new Page object."""
        with self.context.expect_page() as new_page_info:
            self.click(self._NEW_WINDOW_BTN)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    def open_new_window_message(self) -> Page:
        """Click 'New Window Message' and return the new Page object."""
        with self.context.expect_page() as new_page_info:
            self.click(self._NEW_WINDOW_MSG_BTN)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    def get_sample_heading(self, target_page: Page) -> str:
        """Return the heading text from an opened *target_page*."""
        return target_page.locator(self._SAMPLE_HEADING).inner_text()
