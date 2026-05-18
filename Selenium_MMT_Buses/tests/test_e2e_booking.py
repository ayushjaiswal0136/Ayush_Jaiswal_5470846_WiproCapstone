import pytest
import allure

from pages.home_page import HomePage
from pages.bus_search_page import BusSearchPage
from pages.seat_page import SeatPage
from pages.payment_page import PaymentPage

from utils.excel_reader import ExcelReader
from utils.logger import LogGen

logger = LogGen.loggen()

booking_data = ExcelReader.read_excel(
    "passenger_data.xlsx",
    "BookingData"
)

passenger_data = ExcelReader.read_excel(
    "passenger_data.xlsx",
    "PassengerData"
)

payment_data = ExcelReader.read_excel(
    "passenger_data.xlsx",
    "PaymentData"
)


@allure.feature("E2E Bus Booking")
@pytest.mark.parametrize(
    "booking",
    booking_data
)
def test_complete_bus_booking_flow(
    driver,
    booking
):

    passenger = passenger_data[0]

    payment = payment_data[0]

    logger.info("STARTING E2E FLOW")

    # login = LoginPage(driver)
    # login.login()

    home = HomePage(driver)

    home.search_bus(
        booking["from_city"],
        booking["to_city"]
    )

    bus = BusSearchPage(driver)

    # bus.select_bus()
    #
    # seat = SeatPage(driver)
    #
    # seat.fill_passenger_details(
    #     passenger["passenger_name"],
    #     str(passenger["age"]),
    #     str(passenger["mobile"]),
    #     passenger["email"]
    # )
    #
    # payment_page = PaymentPage(driver)
    #
    # payment_page.fill_payment_details(
    #     str(payment["card_number"]),
    #     payment["expiry"],
    #     str(payment["cvv"])
    # )

    bus.verify_bus_search_result()

    logger.info("E2E FLOW COMPLETED")

    assert True