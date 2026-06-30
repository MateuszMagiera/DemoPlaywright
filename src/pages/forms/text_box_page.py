"""Text Box page object — https://demoqa.com/text-box."""

from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import Page

from src.pages.base_page import BasePage


@dataclass
class TextBoxFormData:
    """Data class representing a Text Box form submission."""

    full_name: str
    email: str
    current_address: str
    permanent_address: str


class TextBoxPage(BasePage):
    """Page object for the DemoQA Text Box form page."""

    URL = "https://demoqa.com/text-box"

    # ── Locators ──────────────────────────────────────────────────────────────
    _FULL_NAME_INPUT = "#userName"
    _EMAIL_INPUT = "#userEmail"
    _CURRENT_ADDRESS_INPUT = "#currentAddress"
    _PERMANENT_ADDRESS_INPUT = "#permanentAddress"
    _SUBMIT_BUTTON = "#submit"

    # Output section
    _OUTPUT_NAME = "#name"
    _OUTPUT_EMAIL = "#email"
    _OUTPUT_CURRENT_ADDRESS = "p#currentAddress"
    _OUTPUT_PERMANENT_ADDRESS = "p#permanentAddress"
    _OUTPUT_BOX = "#output"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # ── Actions ───────────────────────────────────────────────────────────────

    def fill_full_name(self, name: str) -> None:
        """Fill the Full Name field."""
        self.fill(self._FULL_NAME_INPUT, name)

    def fill_email(self, email: str) -> None:
        """Fill the Email field."""
        self.fill(self._EMAIL_INPUT, email)

    def fill_current_address(self, address: str) -> None:
        """Fill the Current Address textarea."""
        self.fill(self._CURRENT_ADDRESS_INPUT, address)

    def fill_permanent_address(self, address: str) -> None:
        """Fill the Permanent Address textarea."""
        self.fill(self._PERMANENT_ADDRESS_INPUT, address)

    def submit(self) -> None:
        """Click the Submit button."""
        self.scroll_into_view(self._SUBMIT_BUTTON)
        self.click(self._SUBMIT_BUTTON)

    def fill_all_and_submit(self, data: TextBoxFormData) -> None:
        """Fill all fields with *data* and submit the form."""
        self.fill_full_name(data.full_name)
        self.fill_email(data.email)
        self.fill_current_address(data.current_address)
        self.fill_permanent_address(data.permanent_address)
        self.submit()

    # ── Output readers ────────────────────────────────────────────────────────

    def is_output_visible(self) -> bool:
        """Return True if the output section is displayed."""
        return self.is_visible(self._OUTPUT_BOX)

    def get_output_name(self) -> str:
        """Return the displayed name from the output section."""
        return self.get_text(self._OUTPUT_NAME)

    def get_output_email(self) -> str:
        """Return the displayed email from the output section."""
        return self.get_text(self._OUTPUT_EMAIL)

    def get_output_current_address(self) -> str:
        """Return the displayed current address from the output section."""
        return self.get_text(self._OUTPUT_CURRENT_ADDRESS)

    def get_output_permanent_address(self) -> str:
        """Return the displayed permanent address from the output section."""
        return self.get_text(self._OUTPUT_PERMANENT_ADDRESS)

    def get_email_field_class(self) -> str:
        """Return the CSS class of the email input (used for validation state)."""
        return self.page.locator(self._EMAIL_INPUT).get_attribute("class") or ""
