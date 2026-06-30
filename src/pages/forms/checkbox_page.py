"""Check Box page object — https://demoqa.com/checkbox."""

from __future__ import annotations

from playwright.sync_api import Page

from src.pages.base_page import BasePage


class CheckBoxPage(BasePage):
    """Page object for the DemoQA Check Box page (uses rc-tree widget)."""

    URL = "https://demoqa.com/checkbox"

    # ── Locators ──────────────────────────────────────────────────────────────
    _HOME_CHECKBOX = "span.rc-tree-checkbox[aria-label='Select Home']"
    _CLOSED_SWITCHER = ".rc-tree-switcher_close"
    _RESULT_BOX = "#result"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def expand_all(self) -> None:
        """Expand all tree nodes one at a time, re-querying DOM between each click."""
        for _ in range(30):  # max 30 clicks to avoid infinite loops
            # Re-query each iteration — DOM changes after every click
            count = self.page.locator(self._CLOSED_SWITCHER).count()
            if count == 0:
                break
            # Click first closed switcher only, then re-query
            self.page.locator(self._CLOSED_SWITCHER).first.click(timeout=2000)
            self.page.wait_for_timeout(200)

    def collapse_all(self) -> None:
        """Collapse all tree nodes one at a time, re-querying DOM between each click."""
        open_switcher = ".rc-tree-switcher_open"
        for _ in range(30):
            count = self.page.locator(open_switcher).count()
            if count == 0:
                break
            self.page.locator(open_switcher).first.click(timeout=2000)
            self.page.wait_for_timeout(200)

    def check_home(self) -> None:
        """Check the top-level 'Home' checkbox (selects all)."""
        locator = self.page.locator(self._HOME_CHECKBOX)
        locator.wait_for(state="visible")
        locator.click()

    def check_item_by_label(self, label: str) -> None:
        """Check a specific item by its aria-label (item must be visible/expanded)."""
        checkbox = self.page.locator(f"span.rc-tree-checkbox[aria-label='Select {label}']")
        checkbox.wait_for(state="visible")
        checkbox.click()

    def get_selected_items(self) -> list[str]:
        """Return list of currently selected item names from the result box.

        The result box shows text like:
            You have selected :
            home
            desktop
            ...
        """
        if not self.is_visible(self._RESULT_BOX):
            return []
        raw = self.page.locator(self._RESULT_BOX).inner_text()
        lines = [ln.strip() for ln in raw.splitlines()]
        return [ln for ln in lines if ln and "you have selected" not in ln.lower() and ln != ":"]

    def is_result_visible(self) -> bool:
        """Return True if the result section is visible (some item checked)."""
        return self.is_visible(self._RESULT_BOX)

    def is_item_checked(self, label: str) -> bool:
        """Return True if the item with *label* is in a checked state."""
        checked = self.page.locator(
            f"span.rc-tree-checkbox[aria-label='Select {label}'].rc-tree-checkbox-checked"
        )
        return checked.count() > 0
