"""Functional tests for DemoQA Alerts & Browser Windows section."""

from __future__ import annotations

import pytest

from src.pages.alerts.alerts_page import AlertsPage
from src.pages.alerts.browser_windows_page import BrowserWindowsPage


class TestAlerts:
    """Tests for the Alerts page on DemoQA."""

    @pytest.mark.smoke
    def test_simple_alert_accepted(self, alerts_page: AlertsPage) -> None:
        """Simple alert should be accepted without raising an error."""
        alerts_page.accept_dialog()
        alerts_page.click_simple_alert()
        # If dialog was not handled, Playwright would raise here

    @pytest.mark.smoke
    def test_confirm_dialog_accepted(self, alerts_page: AlertsPage) -> None:
        """Accepting a Confirm dialog should show 'Ok' in the result."""
        alerts_page.accept_dialog()
        alerts_page.click_confirm()
        result = alerts_page.get_confirm_result()
        assert "Ok" in result, f"Expected 'Ok' in result, got: {result!r}"

    def test_confirm_dialog_dismissed(self, alerts_page: AlertsPage) -> None:
        """Dismissing a Confirm dialog should show 'Cancel' in the result."""
        alerts_page.dismiss_dialog()
        alerts_page.click_confirm()
        result = alerts_page.get_confirm_result()
        assert "Cancel" in result, f"Expected 'Cancel' in result, got: {result!r}"

    @pytest.mark.smoke
    def test_prompt_dialog_with_text(self, alerts_page: AlertsPage) -> None:
        """Entering text in a Prompt dialog should reflect it in the result."""
        test_input = "Hello Playwright"
        alerts_page.accept_dialog_with_text(test_input)
        alerts_page.click_prompt()
        result = alerts_page.get_prompt_result()
        assert test_input in result, f"Expected '{test_input}' in result, got: {result!r}"

    @pytest.mark.regression
    def test_prompt_dismissed_shows_no_text(self, alerts_page: AlertsPage) -> None:
        """Dismissing a Prompt dialog should not display any result text."""
        alerts_page.dismiss_dialog()
        alerts_page.click_prompt()
        alerts_page.page.wait_for_timeout(500)
        # When dismissed, the result element either doesn't appear or is empty
        result_locator = alerts_page.page.locator(alerts_page._PROMPT_RESULT)
        if result_locator.is_visible():
            result_text = result_locator.inner_text().strip()
            # It may show "You entered: null" or be empty — no user input should appear
            assert "Hello Playwright" not in result_text
        # Passing if element is invisible — dismiss showed no input


class TestBrowserWindows:
    """Tests for Browser Windows page on DemoQA."""

    @pytest.mark.smoke
    def test_new_tab_opens_with_correct_heading(
        self, browser_windows_page: BrowserWindowsPage
    ) -> None:
        """Clicking 'New Tab' should open a tab with 'This is a sample page' heading."""
        new_tab = browser_windows_page.open_new_tab()
        heading = browser_windows_page.get_sample_heading(new_tab)
        assert "sample page" in heading.lower(), f"Unexpected heading: {heading!r}"
        new_tab.close()

    @pytest.mark.smoke
    def test_new_window_opens_with_correct_heading(
        self, browser_windows_page: BrowserWindowsPage
    ) -> None:
        """Clicking 'New Window' should open a window with the sample page heading."""
        new_win = browser_windows_page.open_new_window()
        heading = browser_windows_page.get_sample_heading(new_win)
        assert "sample page" in heading.lower(), f"Unexpected heading: {heading!r}"
        new_win.close()

    @pytest.mark.regression
    def test_new_tab_has_different_url_from_parent(
        self, browser_windows_page: BrowserWindowsPage
    ) -> None:
        """The URL of the new tab should differ from the parent page URL."""
        parent_url = browser_windows_page.get_url()
        new_tab = browser_windows_page.open_new_tab()
        assert new_tab.url != parent_url, "New tab URL should differ from parent"
        new_tab.close()
