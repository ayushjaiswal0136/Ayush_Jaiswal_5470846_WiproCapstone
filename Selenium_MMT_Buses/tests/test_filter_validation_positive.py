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

# READ SAME CSV FILE
search_data = CSVReader.read_csv("bus_search_data.csv")


@allure.feature("Sleeper Filter")
@allure.story("Verify sleeper filter works successfully")
@pytest.mark.smoke
@pytest.mark.parametrize("data", search_data)
def test_sleeper_filter(driver, data):

    logger.info("========== TEST STARTED : SLEEPER FILTER ==========")

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

    # VERIFY SEARCH RESULT PAGE
    bus = BusSearchPage(driver)

    bus.verify_bus_search_result()

    logger.info("SEARCH RESULT PAGE VERIFIED")

    # =====================================================
    # APPLY SLEEPER FILTER
    # =====================================================

    logger.info("APPLYING SLEEPER FILTER")

    sleeper_filter = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//p[text()='Sleeper']/parent::div"
            )
        )
    )

    # Scrolls webpage until, Sleeper filter element becomes visible
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        sleeper_filter
    )

    # Click
    driver.execute_script(
        "arguments[0].click();",
        sleeper_filter
    )

    logger.info("SLEEPER FILTER CLICKED")

    # =====================================================
    # VERIFY FILTER APPLIED
    # =====================================================

    logger.info("VERIFYING SLEEPER FILTER APPLIED")

    # WAIT FOR ACTIVE CLASS
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[contains(@class,'activeTabs')]//p[text()='Sleeper']"
            )
        )
    )

    active_filter = driver.find_element(
        By.XPATH,
        "//div[contains(@class,'activeTabs')]//p[text()='Sleeper']"
    )

    assert active_filter.is_displayed(), \
        "Sleeper filter not applied"

    logger.info("SLEEPER FILTER VERIFIED SUCCESSFULLY")

    logger.info("========== TEST PASSED ==========")