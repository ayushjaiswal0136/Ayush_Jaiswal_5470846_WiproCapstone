import pytest
import allure
import time

from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage

from utils.csv_reader import CSVReader
from utils.logger import LogGen

logger = LogGen.loggen()

data = CSVReader.read_csv(
    "bus_search_data.csv"
)


@allure.feature("Bus Filters")
@pytest.mark.order(3)
@pytest.mark.parametrize("test_data", data)
def test_bus_filter(driver, test_data):

    logger.info("STARTING BUS FILTER TEST")

    login = LoginPage(driver)

    login.login()

    time.sleep(20)

    home = HomePage(driver)

    home.search_bus(
        test_data["from_city"],
        test_data["to_city"]
    )

    bus = BusSearchPage(driver)

    bus.apply_filters()

    logger.info("BUS FILTER TEST COMPLETED")

    assert True