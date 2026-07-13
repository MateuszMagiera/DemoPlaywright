"""Functional tests for DemoQA Forms section."""

from __future__ import annotations

import allure
import pytest

from src.pages.forms.checkbox_page import CheckBoxPage
from src.pages.forms.radio_button_page import RadioButtonPage
from src.pages.forms.text_box_page import TextBoxFormData, TextBoxPage

# ──────────────────────────────────────────────────────────────────────────────
# Test data
# ──────────────────────────────────────────────────────────────────────────────

VALID_USERS = [
    TextBoxFormData(
        full_name="John Doe",
        email="john.doe@example.com",
        current_address="123 Main St, Springfield",
        permanent_address="456 Oak Ave, Shelbyville",
    ),
    TextBoxFormData(
        full_name="Jane Smith",
        email="jane.smith@test.org",
        current_address="789 Elm Rd",
        permanent_address="789 Elm Rd",
    ),
    TextBoxFormData(
        full_name="Tomasz Kowalski",
        email="t.kowalski@poczta.pl",
        current_address="ul. Krakowska 12, Warszawa",
        permanent_address="ul. Gdańska 7, Kraków",
    ),
]


# ──────────────────────────────────────────────────────────────────────────────
# Text Box tests
# ──────────────────────────────────────────────────────────────────────────────


class TestTextBox:
    """Tests for the Text Box form on DemoQA."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("user", VALID_USERS, ids=[u.full_name for u in VALID_USERS])
    @allure.title("User can submit the text box form")
    @allure.description("Verify all fields are saved and displayed correctly")
    @allure.tag("forms", "smoke")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_submit_all_fields_displays_output(
        self, text_box_page: TextBoxPage, user: TextBoxFormData
    ) -> None:
        """Submitting all fields should display them in the output section."""
        with allure.step("Fill all fields and submit"):
            text_box_page.fill_all_and_submit(user)

        with allure.step("Check output visibility"):
            assert text_box_page.is_output_visible(), "Output box should appear after submit"
        with allure.step("Check output name"):
            assert user.full_name in text_box_page.get_output_name()
        with allure.step("Check output email"):
            assert user.email in text_box_page.get_output_email()
        with allure.step("Check output current address"):
            assert user.current_address in text_box_page.get_output_current_address()
        with allure.step("Check output permanent address"):
            assert user.permanent_address in text_box_page.get_output_permanent_address()

    @pytest.mark.smoke
    @allure.title("User can submit the form with only a name")
    @allure.description("Verify that entering only the full name still produces a visible output")
    @allure.tag("forms", "smoke")
    @allure.severity(allure.severity_level.NORMAL)
    def test_submit_only_name_shows_output(self, text_box_page: TextBoxPage) -> None:
        """Submitting only the name field should still show the output section."""
        with allure.step("Fill only the name field"):
            text_box_page.fill_full_name("Solo Name")
        with allure.step("Submit the form"):
            text_box_page.submit()

        with allure.step("Check output visibility"):
            assert text_box_page.is_output_visible()
        with allure.step("Check output name"):
            assert "Solo Name" in text_box_page.get_output_name()

    def test_invalid_email_shows_error_state(self, text_box_page: TextBoxPage) -> None:
        """An invalid email should give the field an error CSS class."""
        with allure.step("Fill an invalid email"):
            text_box_page.fill_email("not-a-valid-email")
        with allure.step("Submit the form"):
            text_box_page.submit()

        email_class = text_box_page.get_email_field_class()
        with allure.step("Check for error class"):
            assert "field-error" in email_class, f"Expected error class, got: {email_class!r}"

    def test_empty_form_submit_no_output(self, text_box_page: TextBoxPage) -> None:
        """Submitting an empty form should NOT show the output section."""
        with allure.step("Submit an empty form"):
            text_box_page.submit()
        with allure.step("Check output visibility"):
            assert (
                not text_box_page.is_output_visible()
            ), "Output should be hidden for empty submission"

    @pytest.mark.regression
    def test_long_name_accepted(self, text_box_page: TextBoxPage) -> None:
        """A very long name should be accepted and echoed correctly."""
        long_name = "A" * 200
        with allure.step("Fill a very long name"):
            text_box_page.fill_full_name(long_name)
        with allure.step("Submit the form"):
            text_box_page.submit()
        with allure.step("Check output name"):
            assert long_name in text_box_page.get_output_name()

    def test_special_characters_in_address(self, text_box_page: TextBoxPage) -> None:
        """Special characters in address fields should be preserved."""
        data = TextBoxFormData(
            full_name="Test User",
            email="test@test.com",
            current_address='Straße 1 <>&"',
            permanent_address="Ångström Blvd #9",
        )
        with allure.step("Fill all fields and submit"):
            text_box_page.fill_all_and_submit(data)
        with allure.step("Check output current address"):
            assert "Straße" in text_box_page.get_output_current_address()


# ──────────────────────────────────────────────────────────────────────────────
# Check Box tests
# ──────────────────────────────────────────────────────────────────────────────


class TestCheckBox:
    """Tests for the Check Box tree on DemoQA."""

    @pytest.mark.smoke
    def test_check_home_selects_all(self, checkbox_page: CheckBoxPage) -> None:
        """Checking the Home node should select all child items."""
        with allure.step("Check the Home node"):
            checkbox_page.check_home()
        with allure.step("Get selected items"):
            selected = checkbox_page.get_selected_items()
        with allure.step("Check that at least one item is selected"):
            assert len(selected) > 0, "At least one item should be selected"

    def test_expand_all_reveals_nodes(self, checkbox_page: CheckBoxPage) -> None:
        """Expanding all nodes should make child items (Desktop, Documents) visible."""
        with allure.step("Expand all nodes"):
            checkbox_page.expand_all()
        # After expanding, Desktop checkbox should become available
        desktop_cb = checkbox_page.page.locator(
            "span.rc-tree-checkbox[aria-label='Select Desktop']"
        )
        with allure.step("Check that the Desktop node appears"):
            assert desktop_cb.count() > 0, "Desktop node should appear after expand"

    @pytest.mark.regression
    def test_expand_then_collapse(self, checkbox_page: CheckBoxPage) -> None:
        """Expanding and then collapsing should work without errors."""
        with allure.step("Expand all nodes"):
            checkbox_page.expand_all()
        with allure.step("Collapse all nodes"):
            checkbox_page.collapse_all()
        # After collapsing, only the root Home node is visible — result box hidden
        with allure.step("Check that the result box is hidden"):
            assert not checkbox_page.is_result_visible()

    def test_check_desktop_item(self, checkbox_page: CheckBoxPage) -> None:
        """Expanding all and checking 'Desktop' should add it to selected items."""
        with allure.step("Expand all nodes"):
            checkbox_page.expand_all()
        with allure.step("Check the 'Desktop' item"):
            checkbox_page.check_item_by_label("Desktop")
        with allure.step("Get selected items"):
            selected = checkbox_page.get_selected_items()
        with allure.step("Check that some items are selected"):
            assert len(selected) > 0, "Some items should be selected after checking Desktop"


# ──────────────────────────────────────────────────────────────────────────────
# Radio Button tests
# ──────────────────────────────────────────────────────────────────────────────


RADIO_BUTTON_CASES = [
    ("yes", "Yes"),
    ("impressive", "Impressive"),
]


class TestRadioButton:
    """Tests for the Radio Button page on DemoQA."""

    @pytest.mark.smoke
    @pytest.mark.parametrize("action,expected", RADIO_BUTTON_CASES)
    def test_select_radio_shows_confirmation(
        self,
        radio_button_page: RadioButtonPage,
        action: str,
        expected: str,
    ) -> None:
        """Selecting a radio button should show the confirmation text."""
        if action == "yes":
            radio_button_page.select_yes()
        else:
            radio_button_page.select_impressive()

        result = radio_button_page.get_selected_text()
        with allure.step("Check for expected result"):
            assert expected in result, f"Expected '{expected}' in result text, got: {result!r}"

    def test_no_radio_is_disabled(self, radio_button_page: RadioButtonPage) -> None:
        """The 'No' radio button should be disabled on the page."""
        with allure.step("Check that the 'No' radio is disabled"):
            assert radio_button_page.is_no_radio_disabled(), "'No' radio should be disabled"

    @pytest.mark.regression
    def test_selecting_yes_then_impressive_updates_result(
        self, radio_button_page: RadioButtonPage
    ) -> None:
        """Changing radio selection should update the result text accordingly."""
        radio_button_page.select_yes()
        with allure.step("Check that 'Yes' is in the result"):
            assert "Yes" in radio_button_page.get_selected_text()

        radio_button_page.select_impressive()
        with allure.step("Check that 'Impressive' is in the result"):
            assert "Impressive" in radio_button_page.get_selected_text()
