"""Page objects package."""

from src.pages.alerts.alerts_page import AlertsPage
from src.pages.alerts.browser_windows_page import BrowserWindowsPage
from src.pages.base_page import BasePage
from src.pages.forms.checkbox_page import CheckBoxPage
from src.pages.forms.radio_button_page import RadioButtonPage
from src.pages.forms.text_box_page import TextBoxFormData, TextBoxPage
from src.pages.widgets.progress_bar_page import ProgressBarPage
from src.pages.widgets.slider_page import SliderPage
from src.pages.widgets.tabs_page import TabsPage

__all__ = [
    "BasePage",
    "AlertsPage",
    "BrowserWindowsPage",
    "CheckBoxPage",
    "RadioButtonPage",
    "TextBoxFormData",
    "TextBoxPage",
    "ProgressBarPage",
    "SliderPage",
    "TabsPage",
]
