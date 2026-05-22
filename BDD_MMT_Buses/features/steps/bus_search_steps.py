import os
from behave import given, when, then
from locators.home_locators import HomeLocators

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.csv_reader import CsvReader

logger = LogGen.loggen()


# ==========================================
# UNIQUE STEPS FOR BUS SEARCH FEATURE
# ==========================================

@given(u'User extracts test data from CSV "{filename}" for row "{row_num}"')
def step_impl(context, filename, row_num):
    filepath = os.path.join(os.getcwd(), "testdata", filename)
    context.search_data = CsvReader.get_test_data(filepath, row_num)
    assert context.search_data is not None, f"Assertion Failed: Could not load row {row_num} from {filename}"


@when(u'User provides search source city from CSV')
def step_impl(context):
    city = context.search_data.get("from_city")
    HomePage(context.driver).select_city(HomeLocators.FROM_CITY_FIELD, city)


@when(u'User provides search destination city from CSV')
def step_impl(context):
    city = context.search_data.get("to_city")
    HomePage(context.driver).select_city(HomeLocators.TO_CITY_FIELD, city)


@then(u'User should see the correct route from CSV on results page')
def step_impl(context):
    from_city = context.search_data.get("from_city")
    to_city = context.search_data.get("to_city")

    actual_headline = BusSearchPage(context.driver).get_route_title()
    assert from_city.lower() in actual_headline.lower(), f"Assertion Failed: {from_city} not found"
    assert to_city.lower() in actual_headline.lower(), f"Assertion Failed: {to_city} not found"
    assert "bus" in actual_headline.lower(), "Assertion Failed: 'Bus' keyword not found in headline"
    ScreenshotUtil.capture_screenshot(context.driver, "route_verified")


@when(u'User applies the Sleeper filter')
def step_impl(context):
    BusSearchPage(context.driver).filter_sleeper_buses()


@then(u'Verify that the results update successfully')
def step_impl(context):
    is_applied = BusSearchPage(context.driver).is_sleeper_filter_applied()
    assert is_applied, "Assertion Failed: Sleeper filter is not active."
    ScreenshotUtil.capture_screenshot(context.driver, "sleeper_filter_applied")


@when(u'User selects a specific seat to verify')
def step_impl(context):
    BusSearchPage(context.driver).select_seat_and_points_and_continue()


@then(u'Verify that a selected seat number is displayed')
def step_impl(context):
    seat_number = BusSearchPage(context.driver).get_selected_seat_number()
    assert "Seat No" in seat_number, "Assertion Failed: Seat number not displayed on booking page."
    ScreenshotUtil.capture_screenshot(context.driver, "seat_selected")


@then(u'User should see the booking page with correct route details from CSV')
def step_impl(context):
    from_city = context.search_data.get("from_city")
    to_city = context.search_data.get("to_city")

    is_valid = BusSearchPage(context.driver).verify_booking_page_details(from_city, to_city)
    assert is_valid, "Assertion Failed: Route details or heading missing on Review page."
    ScreenshotUtil.capture_screenshot(context.driver, "booking_page_verified")


@then(u'User should see an error message for same source and destination')
def step_impl(context):
    error_msg = HomePage(context.driver).get_same_city_error()
    assert "cannot be same" in error_msg.lower(), "Assertion Failed: Same city error not displayed."
    ScreenshotUtil.capture_screenshot(context.driver, "same_city_error")


@then(u'User should see a No Buses Found message')
def step_impl(context):
    # MMT UI Update: Specific error text removed, leaving an empty container
    is_empty = BusSearchPage(context.driver).is_bus_list_empty()
    assert is_empty, "Assertion Failed: Buses were incorrectly displayed for an invalid route."
    ScreenshotUtil.capture_screenshot(context.driver, "no_buses_found")