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


@allure.feature("Bus Search")
@allure.story("Verify user can search buses successfully")
@pytest.mark.smoke
@pytest.mark.parametrize("data", search_data)
def test_bus_search_headline(driver, data):

    logger.info("========== TEST STARTED : BUS SEARCH HEADLINE ==========")

    # GET DATA FROM CSV
    from_city = data["from_city"]
    to_city = data["to_city"]

    logger.info(f"FROM CITY : {from_city}")
    logger.info(f"TO CITY : {to_city}")

    # HOME PAGE
    home = HomePage(driver)

    # SEARCH BUS
    home.search_bus(from_city, to_city)

    logger.info("BUS SEARCH COMPLETED")

    # BUS SEARCH PAGE
    bus = BusSearchPage(driver)

    # VERIFY RESULT PAGE LOADED
    bus.verify_bus_search_result()

    logger.info("VERIFYING RESULT PAGE HEADLINE")

    # HEADLINE LOCATOR
    headline = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h1[@data-testid='listing-title']"
            )
        )
    )

    # GET HEADLINE TEXT
    actual_headline = headline.text.strip()

    logger.info(f"ACTUAL HEADLINE : {actual_headline}")

    # ASSERTIONS
    logger.info("VERIFYING HEADLINE CONTENT")

    assert from_city.lower() in actual_headline.lower(), \
        f"{from_city} not found in headline"

    assert to_city.lower() in actual_headline.lower(), \
        f"{to_city} not found in headline"

    assert "bus" in actual_headline.lower(), \
        "'Bus' keyword not found in headline"

    logger.info("HEADLINE VERIFIED SUCCESSFULLY")

    logger.info("========== TEST PASSED ==========")