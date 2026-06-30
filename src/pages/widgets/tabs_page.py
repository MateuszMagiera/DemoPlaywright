"""Tabs page object — https://demoqa.com/tabs."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class TabsPage(BasePage):
    """Page object for the DemoQA Tabs widget page."""

    URL = "https://demoqa.com/tabs"

    # ── Locators ──────────────────────────────────────────────────────────────
    _TAB_WHAT = "#demo-tab-what"
    _TAB_ORIGIN = "#demo-tab-origin"
    _TAB_USE = "#demo-tab-use"
    _TAB_MORE = "#demo-tab-more"

    _PANEL_WHAT = "#demo-tabpane-what"
    _PANEL_ORIGIN = "#demo-tabpane-origin"
    _PANEL_USE = "#demo-tabpane-use"
    _PANEL_MORE = "#demo-tabpane-more"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def click_what(self) -> None:
        """Click the 'What' tab."""
        self.click(self._TAB_WHAT)

    def click_origin(self) -> None:
        """Click the 'Origin' tab."""
        self.click(self._TAB_ORIGIN)

    def click_use(self) -> None:
        """Click the 'Use' tab."""
        self.click(self._TAB_USE)

    def click_more(self) -> None:
        """Attempt to click the 'More' tab (disabled on the page)."""
        self.click(self._TAB_MORE)

    # ── Readers ───────────────────────────────────────────────────────────────

    def get_active_tab_name(self) -> str:
        """Return the text of the currently active tab."""
        active = self.page.locator(".nav-tabs .nav-link.active")
        return active.inner_text().strip()

    def get_panel_content(self, tab_name: str) -> str:
        """Return the text content of the given tab's panel."""
        panels = {
            "what": self._PANEL_WHAT,
            "origin": self._PANEL_ORIGIN,
            "use": self._PANEL_USE,
            "more": self._PANEL_MORE,
        }
        selector = panels.get(tab_name.lower(), "")
        if not selector:
            raise ValueError(f"Unknown tab: {tab_name!r}. Expected one of {list(panels)}")
        return self.get_text(selector)

    def is_more_tab_disabled(self) -> bool:
        """Return True if the 'More' tab is disabled."""
        return not self.page.locator(self._TAB_MORE).is_enabled()
