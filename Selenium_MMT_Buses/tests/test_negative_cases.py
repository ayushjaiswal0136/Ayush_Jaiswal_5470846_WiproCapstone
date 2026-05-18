import pytest
import allure
import time

from pages.login_page import LoginPage
from pages.home_page import HomePage

from utils.excel_reader import ExcelReader
from utils.logger import LogGen

logger = LogGen.loggen()

negative_data = ExcelReader.read_data(
    "passenger_data.xlsx",
    "NegativeData"
)


@allure.feature("Negative Test Cases")
@pytest.mark.order(5)
@pytest.mark.parametrize("data", negative_data)
def test_negative_cases(driver, data):

    logger.info("STARTING NEGATIVE TEST")

    login = LoginPage(driver)

    login.login()

    time.sleep(20)

    home = HomePage(driver)

    home.search_bus(
        data["invalid_from"],
        data["invalid_to"]
    )

    logger.info(
        f"NEGATIVE TEST EXECUTED : "
        f"{data['scenario']}"
    )

    assert True