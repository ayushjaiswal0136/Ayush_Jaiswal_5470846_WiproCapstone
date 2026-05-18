import time

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

from utils.logger import LogGen

logger = LogGen.loggen()


class BusSearchPage(BasePage):

    BUS_RESULTS = (
        By.XPATH,
        "//div[contains(@class,'busCardContainer')]"
    )

    def verify_bus_search_result(self):

        logger.info(
            "WAITING FOR BUS SEARCH RESULT PAGE"
        )

        # WAIT FOR SEARCH URL
        WebDriverWait(
            self.driver,
            60
        ).until(
            EC.url_contains(
                "/bus-tickets/search"
            )
        )

        current_url = self.driver.current_url

        logger.info(
            f"CURRENT URL: {current_url}"
        )

        # IMPORTANT FIX
        # WAIT FOR ACTUAL BUS RESULT CARDS
        WebDriverWait(
            self.driver,
            60
        ).until(
            EC.presence_of_element_located(
                self.BUS_RESULTS
            )
        )

        logger.info(
            "BUS RESULTS LOADED SUCCESSFULLY"
        )

        # KEEP PAGE OPEN FOR VISIBILITY
        time.sleep(15)