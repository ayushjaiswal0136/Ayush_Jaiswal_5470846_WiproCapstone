# import pytest
# import allure
#
# from pages.home_page import HomePage
# from pages.bus_search_page import BusSearchPage
# from pages.seat_page import SeatPage
# from pages.payment_page import PaymentPage
#
# from utils.excel_reader import ExcelReader
# from utils.logger import LogGen
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
#
# logger = LogGen.loggen()
#
# booking_data = ExcelReader.read_excel("passenger_data.xlsx", "BookingData")
# passenger_data = ExcelReader.read_excel("passenger_data.xlsx", "PassengerData")
# payment_data = ExcelReader.read_excel("passenger_data.xlsx", "PaymentData")
#
#
# @allure.feature("E2E Bus Booking")
# @pytest.mark.parametrize("booking", booking_data)
# def test_complete_bus_booking_flow(driver, booking):
#     passenger = passenger_data[0]
#     payment = payment_data[0]
#
#     logger.info("STARTING E2E FLOW")
#
#     home = HomePage(driver)
#     home.search_bus(booking["from_city"], booking["to_city"])
#
#     bus = BusSearchPage(driver)
#
#     # Step 1: Verify the list page loads
#     bus.verify_bus_search_result()
#
#     # Step 2: Select the AC layout parameter filter
#     bus.filter_ac_buses()
#
#     # Step 3: Expand the seating map container
#     bus.select_first_bus()
#
#     # Step 4: Click the seat, boarding point, dropping point, and hit continue
#     bus.select_seat_and_points_and_continue()
#
#     # Step 5: Assert the booking headline on the final customer details view
#     logger.info("TEST CASE EXECUTION: ASSERTING SECURE CHECKOUT TITLE HEADLINE")
#
#     WebDriverWait(driver, 45).until(
#         EC.url_contains("/bus/review")
#     )
#     logger.info("TEST CASE EXECUTION: DETECTED ROUTE CHANGE TO SELECTION SUMMARY REVIEW PAGE")
#
#     checkout_header = WebDriverWait(driver, 30).until(
#         EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Complete your booking')]"))
#     )
#
#     header_text = checkout_header.text.strip()
#     logger.info(f"TEST CASE EXECUTION: SUCCESSFUL MATCH CONFIRMED -> '{header_text}'")
#     assert "Complete your booking" in header_text, f"Assertion Failed: Text mismatch, got '{header_text}'"
#     logger.info("TEST CASE EXECUTION: CRITICAL STATUS - PASSED")
#
#     # Step 6: Instantiating Traveller Form profile mappings
#     traveller_form = SeatPage(driver)
#
#     # SAFETY FALLBACK CHECK: Pull values securely with absolute fallbacks
#     passenger_email = passenger.get("email") or passenger.get("Email") or "ayush.jaiswal@example.com"
#     passenger_name = passenger.get("passenger_name") or passenger.get("passenger_name ") or "Ayush Jaiswal"
#     passenger_age = passenger.get("age") or 24
#     passenger_gender = str(passenger.get("gender") or "Male").strip().lower()
#     passenger_mobile = passenger.get("mobile") or passenger.get("Mobile") or "9696850136"
#
#     # Process Traveller Information Block
#     traveller_form.fill_passenger_details(
#         name=passenger_name,
#         age=passenger_age,
#         gender=passenger_gender,
#         mobile=passenger_mobile,
#         email=passenger_email
#     )
#
#     # Process Contact Information Block
#     traveller_form.fill_contact_details(
#         mobile=passenger_mobile,
#         email=passenger_email
#     )
#
#     # Process billing compliance, plan selection options, and fire confirmation submit
#     traveller_form.select_required_options_and_continue()
#     logger.info("TEST CASE EXECUTION: FORM METRICS CONFIGURED AND DISPATCHED TOWARD PAYMENT GATEWAY")
#
#     # ==============================================================================
#     # NEW CODE: ADDED PAYMENT STEP BELOW (Previous logic completely untouched)
#     # ==============================================================================
#
#     # Step 7: Final Phase - Payment Page Interactions
#     logger.info("TEST CASE EXECUTION: INITIALIZING PAYMENT PAGE PROTOCOLS")
#
#     # Wait for URL to shift to the checkout gateway
#     WebDriverWait(driver, 45).until(
#         EC.url_contains("/checkout")
#     )
#     logger.info("TEST CASE EXECUTION: SECURE PAYMENT GATEWAY LOADED")
#
#     payment_form = PaymentPage(driver)
#
#     # SAFETY FALLBACK CHECK: Safely extract payment data matching your previous style
#     card_num = payment.get("card_number") or payment.get("card_number ") or "4111111111111111"
#     expiry = payment.get("expiry") or payment.get("Expiry") or "12/28"
#     cvv = payment.get("cvv") or payment.get("CVV") or "123"
#     card_name = payment.get("card_holder") or payment.get("card_holder ") or "AYUSH JAISWAL"
#
#     # Execute Payment Steps
#     payment_form.select_credit_card_option()
#     payment_form.enter_card_details(card_num, expiry, cvv, card_name)
#
#     logger.info("TEST CASE EXECUTION: ALL DATA INJECTED EXCLUSIVELY FROM EXCEL. E2E AUTOMATION COMPLETE.")
#
#     # Final retention visibility pause frame context
#     logger.info("TEST CASE EXECUTION: ENGAGING 5-SECOND RETENTION PAUSE BEFORE CLOSING...")
#     time.sleep(5)
#
#     logger.info("E2E FLOW COMPLETED")

# ___________________________________________________

import pytest
import allure

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from pages.seat_page import SeatPage
from pages.payment_page import PaymentPage

from utils.excel_reader import ExcelReader
from utils.logger import LogGen

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

logger = LogGen.loggen()

# READ SINGLE SHEET DATA
booking_data = ExcelReader.read_excel(
    "bookingdata.xlsx",
    "Sheet1"
)


@allure.feature("E2E Bus Booking")
@pytest.mark.parametrize("booking", booking_data)
def test_complete_bus_booking_flow(driver, booking):

    logger.info("STARTING E2E FLOW")

    # GET DATA FROM EXCEL
    from_city = booking["from_city"]
    to_city = booking["to_city"]

    passenger_name = booking["passenger_name"]
    passenger_age = booking["age"]
    passenger_gender = booking["gender"]

    passenger_mobile = booking["mobile"]
    passenger_email = booking["email"]

    card_num = booking["card_number"]
    expiry = booking["expiry"]
    cvv = booking["cvv"]

    # HOME PAGE
    home = HomePage(driver)

    home.search_bus(
        from_city,
        to_city
    )

    # SAFE ASSERT
    current_url = driver.current_url

    assert "search" in current_url.lower(), \
        "Search page not opened"

    logger.info("SEARCH PAGE URL VERIFIED")

    # BUS SEARCH PAGE
    bus = BusSearchPage(driver)

    # VERIFY SEARCH RESULT
    bus.verify_bus_search_result()

    # APPLY AC FILTER
    bus.filter_ac_buses()

    # SELECT FIRST BUS
    bus.select_first_bus()

    # SELECT SEAT + BOARDING + CONTINUE
    bus.select_seat_and_points_and_continue()

    # VERIFY BOOKING PAGE
    logger.info(
        "ASSERTING BOOKING PAGE HEADER"
    )

    WebDriverWait(driver, 45).until(
        EC.url_contains("/bus/review")
    )

    checkout_header = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'Complete your booking')]"
            )
        )
    )

    header_text = checkout_header.text.strip()

    logger.info(
        f"HEADER FOUND : {header_text}"
    )

    # SAFE ASSERT
    assert "Complete your booking" in header_text, \
        f"Wrong header found: {header_text}"

    logger.info("BOOKING PAGE VERIFIED")

    # SEAT PAGE
    traveller_form = SeatPage(driver)

    # FILL PASSENGER DETAILS
    traveller_form.fill_passenger_details(
        name=passenger_name,
        age=passenger_age,
        gender=passenger_gender,
        mobile=passenger_mobile,
        email=passenger_email
    )

    # FILL CONTACT DETAILS
    traveller_form.fill_contact_details(
        mobile=passenger_mobile,
        email=passenger_email
    )

    # CONTINUE TO PAYMENT
    traveller_form.select_required_options_and_continue()

    logger.info(
        "PASSENGER DETAILS SUBMITTED"
    )

    # PAYMENT PAGE
    logger.info(
        "OPENING PAYMENT PAGE"
    )

    WebDriverWait(driver, 45).until(
        EC.url_contains("/checkout")
    )

    logger.info(
        "PAYMENT PAGE OPENED"
    )

    # SAFE ASSERT
    payment_url = driver.current_url

    assert "/checkout" in payment_url, \
        "Payment page not opened"

    logger.info("PAYMENT PAGE VERIFIED")

    payment_form = PaymentPage(driver)

    # SELECT CREDIT CARD
    payment_form.select_credit_card_option()

    # ENTER CARD DETAILS
    payment_form.enter_card_details(
        card_num,
        expiry,
        cvv,
        passenger_name
    )

    logger.info(
        "PAYMENT DETAILS ENTERED SUCCESSFULLY"
    )

    # FINAL WAIT
    time.sleep(5)

    logger.info("E2E FLOW COMPLETED")