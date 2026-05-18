import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

from utils.config_reader import ConfigReader
from utils.logger import LogGen

logger = LogGen.loggen()


class LoginPage(BasePage):

    LOGIN_BTN = (
        By.XPATH,
        "//p[text()='Login or Create Account']"
    )

    MOBILE_INPUT = (
        By.XPATH,
        "//input[@placeholder='Enter Mobile Number']"
    )

    CONTINUE_BTN = (
        By.XPATH,
        "//button[contains(.,'Continue')]"
    )

    def login(self):

        logger.info("OPENING LOGIN POPUP")

        time.sleep(5)

        self.driver.execute_script(
            "window.scrollTo(0,0);"
        )

        login_btn = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.element_to_be_clickable(
                self.LOGIN_BTN
            )
        )

        login_btn.click()

        logger.info("ENTERING MOBILE NUMBER")

        mobile_input = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.visibility_of_element_located(
                self.MOBILE_INPUT
            )
        )

        mobile_input.clear()

        mobile_input.send_keys(
            ConfigReader.get("mobile_number")
        )

        time.sleep(2)

        logger.info("CLICKING CONTINUE")

        continue_btn = WebDriverWait(
            self.driver,
            30
        ).until(
            EC.element_to_be_clickable(
                self.CONTINUE_BTN
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            continue_btn
        )

        time.sleep(1)

        continue_btn.click()

        logger.info("WAITING FOR OTP")

        input(
            "ENTER OTP MANUALLY THEN PRESS ENTER HERE..."
        )

        logger.info("LOGIN SUCCESS")