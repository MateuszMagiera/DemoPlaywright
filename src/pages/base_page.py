"""Base Page Object — all page objects inherit from this class."""

from __future__ import annotations

from pathlib import Path

from playwright.sync_api import Locator, Page


class BasePage:
    """Base class providing common helpers for all Page Objects.

    Usage:
        class MyPage(BasePage):
            URL = "https://example.com/my-page"
    """

    URL: str = ""

    def __init__(self, page: Page) -> None:
        self.page = page

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> None:
        """Navigate to this page's URL and wait for network to idle."""
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def reload(self) -> None:
        """Reload the current page."""
        self.page.reload()
        self.page.wait_for_load_state("networkidle")

    # ── Element helpers (all with built-in waits) ─────────────────────────────

    def click(self, selector: str) -> None:
        """Click an element identified by *selector*."""
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        """Clear and fill an input element."""
        locator = self.page.locator(selector)
        locator.clear()
        locator.fill(value)

    def get_text(self, selector: str) -> str:
        """Return the visible text content of an element."""
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        """Return True if the element matching *selector* is visible."""
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """Return True if the element matching *selector* is enabled."""
        return self.page.locator(selector).is_enabled()

    def wait_for_selector(self, selector: str, *, timeout: float | None = None) -> Locator:
        """Wait until element is visible and return its Locator."""
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout)
        return locator

    def select_option(self, selector: str, value: str) -> None:
        """Select an option from a <select> element by its *value*."""
        self.page.locator(selector).select_option(value)

    def check(self, selector: str) -> None:
        """Check a checkbox or radio button."""
        self.page.locator(selector).check()

    def uncheck(self, selector: str) -> None:
        """Uncheck a checkbox."""
        self.page.locator(selector).uncheck()

    def hover(self, selector: str) -> None:
        """Hover the mouse over an element."""
        self.page.locator(selector).hover()

    def scroll_into_view(self, selector: str) -> None:
        """Scroll element into the viewport."""
        self.page.locator(selector).scroll_into_view_if_needed()

    # ── Assertions (lightweight, Playwright-native) ───────────────────────────

    def expect_url_contains(self, fragment: str) -> None:
        """Assert the current URL contains *fragment*."""
        from playwright.sync_api import expect

        expect(self.page).to_have_url(f".*{fragment}.*")

    def expect_visible(self, selector: str) -> None:
        """Assert an element is visible."""
        from playwright.sync_api import expect

        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, expected: str) -> None:
        """Assert an element contains *expected* text."""
        from playwright.sync_api import expect

        expect(self.page.locator(selector)).to_contain_text(expected)

    # ── Screenshots ───────────────────────────────────────────────────────────

    def screenshot(self, name: str, *, full_page: bool = True) -> Path:
        """Capture and save a screenshot; return its Path."""
        screenshots_dir = Path("reports/screenshots")
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        path = screenshots_dir / f"{name}.png"
        self.page.screenshot(path=str(path), full_page=full_page)
        return path

    # ── Scroll utilities ──────────────────────────────────────────────────────

    def scroll_to_bottom(self) -> None:
        """Scroll to the bottom of the page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        """Scroll back to the top of the page."""
        self.page.evaluate("window.scrollTo(0, 0)")
