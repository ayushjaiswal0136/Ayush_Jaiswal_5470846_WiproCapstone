import pytest
import allure

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage

from utils.csv_reader import CSVReader
from utils.logger import LogGen

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = LogGen.loggen()

# READ CSV DATA
search_data = CSVReader.read_csv("bus_search_data.csv")


@allure.feature("Booking Page")
@allure.story("Verify booking page opens with correct bus details")
@pytest.mark.smoke
@pytest.mark.parametrize("data", search_data)
def test_booking_page_bus_details(driver, data):

    logger.info("========== TEST STARTED : BOOKING PAGE ==========")

    # GET DATA FROM CSV
    from_city = data["from_city"]
    to_city = data["to_city"]

    logger.info(f"FROM CITY : {from_city}")
    logger.info(f"TO CITY : {to_city}")

    # =====================================================
    # SEARCH BUS
    # =====================================================

    home = HomePage(driver)

    home.search_bus(from_city, to_city)

    logger.info("BUS SEARCH COMPLETED")

    # =====================================================
    # RESULT PAGE
    # =====================================================

    bus = BusSearchPage(driver)

    bus.verify_bus_search_result()

    logger.info("RESULT PAGE VERIFIED")

    # =====================================================
    # SELECT FIRST BUS
    # =====================================================

    bus.select_first_bus()

    logger.info("FIRST BUS SELECTED")

    # =====================================================
    # SELECT SEAT + BOARDING + DROPPING + CONTINUE
    # =====================================================

    bus.select_seat_and_points_and_continue()

    logger.info("SEAT AND POINTS SELECTED")

    # =====================================================
    # VERIFY COMPLETE YOUR BOOKING PAGE
    # =====================================================

    logger.info("VERIFYING BOOKING PAGE")

    WebDriverWait(driver, 40).until(
        EC.url_contains("/bus/review")
    )

    logger.info("BOOKING PAGE URL VERIFIED")

    # VERIFY PAGE HEADING
    booking_heading = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h1[contains(text(),'Complete your booking')]"
            )
        )
    )

    assert booking_heading.is_displayed(), \
        "'Complete your booking' heading not visible"

    logger.info("BOOKING PAGE HEADING VERIFIED")

    # =====================================================
    # VERIFY FROM AND TO CITY PRESENT
    # =====================================================

    logger.info("VERIFYING ROUTE DETAILS")

    page_source = driver.page_source.lower()

    assert from_city.lower() in page_source, \
        f"{from_city} not found on booking page"

    assert to_city.lower() in page_source, \
        f"{to_city} not found on booking page"

    logger.info("COMPLETE YOUR BOOKING HEADLINE VERIFIED SUCCESSFULLY")

    logger.info("========== TEST PASSED ==========")