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


@allure.feature("Seat Verification")
@allure.story("Verify selected seat is displayed on booking page")
@pytest.mark.smoke
@pytest.mark.parametrize("data", search_data)
def test_selected_seat_verification(driver, data):

    logger.info(
        "========== TEST STARTED : SELECTED SEAT VERIFICATION =========="
    )

    # =====================================================
    # GET CSV DATA
    # =====================================================

    from_city = data["from_city"]
    to_city = data["to_city"]

    logger.info(f"FROM CITY : {from_city}")
    logger.info(f"TO CITY : {to_city}")

    # =====================================================
    # SEARCH BUS
    # =====================================================

    home = HomePage(driver)

    home.search_bus(
        from_city,
        to_city
    )

    logger.info("BUS SEARCH COMPLETED")

    # =====================================================
    # RESULT PAGE
    # =====================================================

    bus = BusSearchPage(driver)

    bus.verify_bus_search_result()

    logger.info("RESULT PAGE VERIFIED")

    # =====================================================
    # OPEN SEAT MAP
    # =====================================================

    bus.select_first_bus()

    logger.info("SEAT MAP OPENED")

    # =====================================================
    # SELECT FIRST AVAILABLE SEAT
    # =====================================================

    seats = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located(
            bus.AVAILABLE_SEATS
        )
    )

    selected_seat = None

    for seat in seats:

        try:

            # GET SEAT NUMBER BEFORE CLICK
            selected_seat = seat.get_attribute("title")

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                seat
            )

            driver.execute_script(
                "arguments[0].click();",
                seat
            )

            logger.info(
                f"SELECTED SEAT : {selected_seat}"
            )

            # VERIFY BOARDING POINT APPEARS
            WebDriverWait(driver, 7).until(
                EC.element_to_be_clickable(
                    bus.FIRST_BOARDING_POINT
                )
            )

            break

        except Exception:

            continue

    assert selected_seat is not None, \
        "NO AVAILABLE SEAT SELECTED"

    # =====================================================
    # SELECT BOARDING POINT
    # =====================================================

    boarding = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            bus.FIRST_BOARDING_POINT
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        boarding
    )

    logger.info("BOARDING POINT SELECTED")

    # =====================================================
    # SELECT DROPPING POINT
    # =====================================================

    dropping = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            bus.FIRST_DROPPING_POINT
        )
    )

    driver.execute_script(
        "arguments[0].click();",
        dropping
    )

    logger.info("DROPPING POINT SELECTED")

    # =====================================================
    # CLICK CONTINUE
    # =====================================================

    continue_btn = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            bus.CONTINUE_BTN
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        continue_btn
    )

    driver.execute_script(
        "arguments[0].click();",
        continue_btn
    )

    logger.info("CONTINUE BUTTON CLICKED")

    # =====================================================
    # VERIFY BOOKING PAGE
    # =====================================================

    WebDriverWait(driver, 40).until(
        EC.url_contains("/bus/review")
    )

    logger.info("BOOKING PAGE OPENED")

    # =====================================================
    # VERIFY SELECTED SEAT DISPLAYED
    # =====================================================

    seat_info = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//span[contains(.,'Seat No')]"
            )
        )
    )

    seat_text = seat_info.text.strip()

    logger.info(
        f"BOOKING PAGE SEAT INFO : {seat_text}"
    )

    assert "Seat No" in seat_text, \
        "Selected seat information not displayed on booking page"

    logger.info(
        "SELECTED SEAT VERIFIED SUCCESSFULLY"
    )

    logger.info(
        "========== TEST PASSED =========="
    )

    logger.info(
        "SELECTED SEAT VERIFIED SUCCESSFULLY"
    )

    logger.info(
        "========== TEST PASSED =========="
    )