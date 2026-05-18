import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

from utils.logger import LogGen

logger = LogGen.loggen()


class PaymentPage(BasePage):

    CARD_NUMBER = (
        By.XPATH,
        "//input[contains(@placeholder,'Card')]"
    )

    EXPIRY = (
        By.XPATH,
        "//input[contains(@placeholder,'MM/YY')]"
    )

    CVV = (
        By.XPATH,
        "//input[contains(@placeholder,'CVV')]"
    )

    def fill_payment_details(
        self,
        card,
        expiry,
        cvv
    ):

        logger.info("FILLING PAYMENT DETAILS")

        time.sleep(5)

        self.type(self.CARD_NUMBER, card)

        self.type(self.EXPIRY, expiry)

        self.type(self.CVV, cvv)

        logger.info("PAYMENT PAGE COMPLETED")