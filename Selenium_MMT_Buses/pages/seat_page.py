import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

from utils.logger import LogGen

logger = LogGen.loggen()


class SeatPage(BasePage):

    FIRST_SEAT = (
        By.XPATH,
        "(//div[contains(@class,'seat')])[1]"
    )

    CONTINUE_BTN = (
        By.XPATH,
        "//button[contains(text(),'Continue')]"
    )

    NAME = (
        By.XPATH,
        "//input[@placeholder='Name']"
    )

    AGE = (
        By.XPATH,
        "//input[@placeholder='Age']"
    )

    MOBILE = (
        By.XPATH,
        "//input[@placeholder='Mobile Number']"
    )

    EMAIL = (
        By.XPATH,
        "//input[@placeholder='Email']"
    )

    def fill_passenger_details(
        self,
        name,
        age,
        mobile,
        email
    ):

        logger.info("SELECTING SEAT")

        time.sleep(5)

        self.click(self.FIRST_SEAT)

        time.sleep(2)

        logger.info("FILLING PASSENGER DETAILS")

        self.type(self.NAME, name)

        self.type(self.AGE, age)

        self.type(self.MOBILE, mobile)

        self.type(self.EMAIL, email)

        logger.info("CLICKING CONTINUE")

        self.click(self.CONTINUE_BTN)

        time.sleep(5)