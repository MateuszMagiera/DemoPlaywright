"""Functional tests for DemoQA Widgets section."""

from __future__ import annotations

import pytest

from src.pages.widgets.progress_bar_page import ProgressBarPage
from src.pages.widgets.slider_page import SliderPage
from src.pages.widgets.tabs_page import TabsPage


class TestSlider:
    """Tests for the Slider widget on DemoQA."""

    @pytest.mark.smoke
    def test_default_value_is_within_range(self, slider_page: SliderPage) -> None:
        """Slider should start with a value between min and max."""
        value = slider_page.get_current_value()
        min_val = slider_page.get_min()
        max_val = slider_page.get_max()
        assert min_val <= value <= max_val, f"Default value {value} not in [{min_val}, {max_val}]"

    @pytest.mark.parametrize("target", [0, 25, 50, 75, 100])
    def test_set_slider_value(self, slider_page: SliderPage, target: int) -> None:
        """Setting slider to *target* should update the displayed value."""
        slider_page.set_value(target)
        assert slider_page.get_current_value() == target

    @pytest.mark.regression
    def test_min_and_max_boundaries(self, slider_page: SliderPage) -> None:
        """Slider min should be 0 and max should be 100."""
        assert slider_page.get_min() == 0
        assert slider_page.get_max() == 100


class TestProgressBar:
    """Tests for the Progress Bar widget on DemoQA."""

    @pytest.mark.smoke
    def test_starts_at_zero(self, progress_bar_page: ProgressBarPage) -> None:
        """Progress bar should start at 0 before being started."""
        assert progress_bar_page.get_value() == 0

    @pytest.mark.slow
    def test_progress_reaches_100(self, progress_bar_page: ProgressBarPage) -> None:
        """Progress bar should reach 100% and reveal the Reset button."""
        progress_bar_page.start()
        progress_bar_page.wait_until_complete(timeout=20_000)

        assert progress_bar_page.get_value() == 100
        assert progress_bar_page.is_reset_visible()

    @pytest.mark.slow
    def test_reset_resets_to_zero(self, progress_bar_page: ProgressBarPage) -> None:
        """After reaching 100%, clicking Reset should return value to 0."""
        progress_bar_page.start()
        progress_bar_page.wait_until_complete(timeout=20_000)
        progress_bar_page.reset()

        assert progress_bar_page.get_value() == 0

    def test_stop_pauses_progress(self, progress_bar_page: ProgressBarPage) -> None:
        """Stopping mid-way should freeze the progress bar value."""
        progress_bar_page.start()
        # Let it advance a bit
        progress_bar_page.page.wait_for_timeout(1_500)
        progress_bar_page.stop()

        value_after_stop = progress_bar_page.get_value()
        progress_bar_page.page.wait_for_timeout(1_000)
        value_after_wait = progress_bar_page.get_value()

        assert value_after_stop == value_after_wait, "Progress bar should not advance while stopped"


class TestTabs:
    """Tests for the Tabs widget on DemoQA."""

    @pytest.mark.smoke
    def test_what_tab_is_active_by_default(self, tabs_page: TabsPage) -> None:
        """The 'What' tab should be active when the page first loads."""
        assert tabs_page.get_active_tab_name() == "What"

    @pytest.mark.parametrize(
        "tab,keyword",
        [
            ("what", "Lorem Ipsum"),
            ("origin", "Lorem Ipsum"),
            ("use", "Lorem Ipsum"),
        ],
    )
    def test_each_tab_shows_content(self, tabs_page: TabsPage, tab: str, keyword: str) -> None:
        """Clicking each tab should reveal its content panel."""
        if tab == "origin":
            tabs_page.click_origin()
        elif tab == "use":
            tabs_page.click_use()
        # 'what' is default, no click needed

        content = tabs_page.get_panel_content(tab)
        assert len(content) > 0, f"Panel '{tab}' should have content"

    def test_more_tab_is_disabled(self, tabs_page: TabsPage) -> None:
        """The 'More' tab should be disabled on the DemoQA page."""
        assert tabs_page.is_more_tab_disabled(), "'More' tab should be disabled"

    @pytest.mark.regression
    def test_switching_tabs_changes_active(self, tabs_page: TabsPage) -> None:
        """Clicking 'Origin' should make it the active tab."""
        tabs_page.click_origin()
        assert tabs_page.get_active_tab_name() == "Origin"
