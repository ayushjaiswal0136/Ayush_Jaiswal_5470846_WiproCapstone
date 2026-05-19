import pytest
import allure

from pages.home_page import HomePage
from utils.csv_reader import CSVReader
from utils.logger import LogGen

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = LogGen.loggen()

# READ CSV DATA
negative_data = CSVReader.read_csv(
    "negative_bus_search_data.csv"
)


@allure.feature("Negative Testing")
@allure.story("Verify error for same source and destination")
@pytest.mark.parametrize("data", negative_data)
def test_same_source_destination(driver, data):

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
    # HOME PAGE
    # =====================================================

    home = HomePage(driver)

    # CLOSE POPUP
    home.close_popup()

    # CLICK BUS TAB
    home.select_bus_tab()

    # LOCATORS
    from_field = (
        By.ID,
        "fromCity"
    )

    to_field = (
        By.ID,
        "toCity"
    )

    # ENTER FROM CITY
    home.select_city(
        from_field,
        from_city
    )

    # ENTER TO CITY
    home.select_city(
        to_field,
        to_city
    )

    logger.info(
        "SAME SOURCE AND DESTINATION ENTERED"
    )

    # =====================================================
    # VERIFY ERROR MESSAGE
    # =====================================================

    error_message = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//span[contains(@class,'errorMsgText')]"
            )
        )
    )

    actual_error = error_message.text.strip()

    logger.info(
        f"ERROR MESSAGE : {actual_error}"
    )

    assert (
        "cannot be same" in actual_error
    ), "VALIDATION ERROR MESSAGE NOT DISPLAYED"

    logger.info(
        "NEGATIVE TEST PASSED SUCCESSFULLY"
    )

    logger.info(
        "========== TEST PASSED =========="
    )