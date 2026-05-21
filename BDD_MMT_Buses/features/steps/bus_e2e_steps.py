import allure
import os
from behave import given, when, then
from locators.home_locators import HomeLocators

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from pages.seat_page import SeatPage
from pages.payment_page import PaymentPage

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.excel_reader import ExcelReader

logger = LogGen.loggen()


@given(u'User launches MakeMyTrip application')
def step_impl(context):
    logger.info("Application Launched via environment.py")


@given(u'User loads test data from Excel "{filename}"')
def step_impl(context, filename):
    # Construct absolute path to the testdata folder
    filepath = os.path.join(os.getcwd(), "testdata", filename)
    context.test_data = ExcelReader.get_test_data(filepath)


@when(u'User closes the login popup')
def step_impl(context):
    HomePage(context.driver).close_popup()


@when(u'User navigates to the Bus section')
def step_impl(context):
    HomePage(context.driver).select_bus_tab()


@when(u'User enters source city from Excel')
def step_impl(context):
    city = context.test_data.get("from_city")
    HomePage(context.driver).select_city(HomeLocators.FROM_CITY_FIELD, city)


@when(u'User enters destination city from Excel')
def step_impl(context):
    city = context.test_data.get("to_city")
    HomePage(context.driver).select_city(HomeLocators.TO_CITY_FIELD, city)


@when(u'User selects a travel date')
def step_impl(context):
    HomePage(context.driver).select_date()


@when(u'User clicks on Search Buses button')
def step_impl(context):
    HomePage(context.driver).click_search()
    BusSearchPage(context.driver).verify_bus_search_result()


@when(u'User applies the AC filter')
def step_impl(context):
    BusSearchPage(context.driver).filter_ac_buses()


@when(u'User selects an available bus')
def step_impl(context):
    BusSearchPage(context.driver).select_first_bus()


@when(u'User selects a specific seat')
def step_impl(context):
    pass


@when(u'User verifies boarding and dropping points')
def step_impl(context):
    BusSearchPage(context.driver).select_seat_and_points_and_continue()


@when(u'User enters passenger details from Excel')
def step_impl(context):
    seat_page = SeatPage(context.driver)

    name = context.test_data.get("passenger_name")
    age = context.test_data.get("age")
    mobile = context.test_data.get("mobile")
    email = context.test_data.get("email")
    gender = "Male"  # Not in Excel, defaulting to Male

    seat_page.fill_passenger_details(name, age, gender)
    seat_page.fill_contact_details(mobile, email)
    ScreenshotUtil.capture_screenshot(context.driver, "passenger_details")


@when(u'User proceeds to payment page')
def step_impl(context):
    SeatPage(context.driver).select_required_options_and_continue()


@when(u'User enters card details from Excel')
def step_impl(context):
    payment_page = PaymentPage(context.driver)
    payment_page.select_credit_card_option()

    card_number = context.test_data.get("card_number")
    card_holder = context.test_data.get("card_holder")
    expiry = context.test_data.get("expiry")
    cvv = "123"  # Not in Excel, defaulting to 123

    # Format the expiry date properly in case Excel returns a serial number or datetime object
    if isinstance(expiry, int) or isinstance(expiry, float):
        # If your excel value '46386' causes issues, format the column as plain Text in Excel (e.g., '12/28')
        expiry = str(expiry)
    elif hasattr(expiry, "strftime"):
        expiry = expiry.strftime("%m/%y")

    payment_page.enter_card_details(card_number, expiry, cvv, card_holder)
    ScreenshotUtil.capture_screenshot(context.driver, "card_entered")


@then(u'Close the browser')
def step_impl(context):
    logger.info("End of E2E Flow. Browser will close via environment.py")