import pytest
import allure
import time

from pages.login_page import LoginPage
from pages.home_page import HomePage

from utils.csv_reader import CSVReader
from utils.logger import LogGen

logger = LogGen.loggen()

data = CSVReader.read_csv(
    "bus_search_data.csv"
)


@allure.feature("Bus Search")
@pytest.mark.order(2)
@pytest.mark.parametrize("test_data", data)
def test_bus_search(driver, test_data):

    logger.info("STARTING BUS SEARCH TEST")

    login = LoginPage(driver)

    login.login()

    time.sleep(20)

    home = HomePage(driver)

    home.search_bus(
        test_data["from_city"],
        test_data["to_city"]
    )

    logger.info(
        f"BUS SEARCH SUCCESSFUL : "
        f"{test_data['from_city']} "
        f"TO "
        f"{test_data['to_city']}"
    )

    assert True