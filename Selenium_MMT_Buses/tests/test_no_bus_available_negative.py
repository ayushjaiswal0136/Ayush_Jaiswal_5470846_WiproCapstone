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
negative_data = CSVReader.read_csv(
    "no_bus_route_data.csv"
)


@allure.feature("Negative Testing")
@allure.story("Verify no bus available message")
@pytest.mark.parametrize("data", negative_data)
def test_no_bus_available(driver, data):

    logger.info(
        "========== NEGATIVE TEST STARTED =========="
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

    logger.info(
        "BUS SEARCH COMPLETED"
    )

    # =====================================================
    # VERIFY NO BUS MESSAGE
    # =====================================================

    no_bus_message = WebDriverWait(driver, 40).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'No bus found on this route')]"
            )
        )
    )

    actual_message = no_bus_message.text.strip()

    logger.info(
        f"NO BUS MESSAGE : {actual_message}"
    )

    assert (
        "No bus found on this route" in actual_message
    ), "NO BUS MESSAGE NOT DISPLAYED"

    logger.info("NO BUS FOUND NEGATIVE TEST PASSED SUCCESSFULLY")

    logger.info(
        "========== TEST PASSED =========="
    )