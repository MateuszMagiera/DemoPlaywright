"""Shared fixtures for functional tests."""

from __future__ import annotations

import pytest
from playwright.sync_api import BrowserContext, Page

from src.pages.alerts.alerts_page import AlertsPage
from src.pages.alerts.browser_windows_page import BrowserWindowsPage
from src.pages.forms.checkbox_page import CheckBoxPage
from src.pages.forms.radio_button_page import RadioButtonPage
from src.pages.forms.text_box_page import TextBoxPage
from src.pages.widgets.progress_bar_page import ProgressBarPage
from src.pages.widgets.slider_page import SliderPage
from src.pages.widgets.tabs_page import TabsPage


@pytest.fixture
def text_box_page(page: Page) -> TextBoxPage:
    """Navigate to and return the Text Box page object."""
    po = TextBoxPage(page)
    po.navigate()
    return po


@pytest.fixture
def checkbox_page(page: Page) -> CheckBoxPage:
    """Navigate to and return the Check Box page object."""
    po = CheckBoxPage(page)
    po.navigate()
    return po


@pytest.fixture
def radio_button_page(page: Page) -> RadioButtonPage:
    """Navigate to and return the Radio Button page object."""
    po = RadioButtonPage(page)
    po.navigate()
    return po


@pytest.fixture
def slider_page(page: Page) -> SliderPage:
    """Navigate to and return the Slider widget page object."""
    po = SliderPage(page)
    po.navigate()
    return po


@pytest.fixture
def progress_bar_page(page: Page) -> ProgressBarPage:
    """Navigate to and return the Progress Bar widget page object."""
    po = ProgressBarPage(page)
    po.navigate()
    return po


@pytest.fixture
def tabs_page(page: Page) -> TabsPage:
    """Navigate to and return the Tabs widget page object."""
    po = TabsPage(page)
    po.navigate()
    return po


@pytest.fixture
def alerts_page(page: Page) -> AlertsPage:
    """Navigate to and return the Alerts page object."""
    po = AlertsPage(page)
    po.navigate()
    return po


@pytest.fixture
def browser_windows_page(page: Page, context: BrowserContext) -> BrowserWindowsPage:
    """Navigate to and return the Browser Windows page object."""
    po = BrowserWindowsPage(page, context)
    po.navigate()
    return po
