import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import LogGen

logger = LogGen.loggen()


class HomePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            5
        )

    def close_popup(self):

        try:

            time.sleep(2)

            close_btn = self.driver.find_element(
                By.XPATH,
                "//span[@data-cy='closeModal']"
            )

            self.driver.execute_script(
                "arguments[0].click();",
                close_btn
            )

            logger.info(
                "LOGIN POPUP CLOSED"
            )

            time.sleep(1)

        except:

            try:

                body = self.driver.find_element(
                    By.TAG_NAME,
                    "body"
                )

                body.click()

                logger.info(
                    "CLICKED OUTSIDE POPUP"
                )

                time.sleep(1)

            except:

                logger.info(
                    "NO POPUP FOUND"
                )

    def select_bus_tab(self):

        try:

            bus_tab = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//span[contains(text(),'Buses')]"
                    )
                )
            )

            self.driver.execute_script(
                "arguments[0].click();",
                bus_tab
            )

            logger.info(
                "BUS TAB CLICKED"
            )

            time.sleep(2)

        except Exception as e:

            logger.info(
                f"BUS TAB ISSUE: {str(e)}"
            )

    def select_city(self, field, city):

        city_box = self.wait.until(
            EC.element_to_be_clickable(field)
        )

        # ORIGINAL: Keep JS click to bypass overlapping UI elements
        self.driver.execute_script(
            "arguments[0].click();",
            city_box
        )

        logger.info(
            f"CLICKED FIELD: {city}"
        )

        time.sleep(2)

        active_input = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[contains(@placeholder,'From') or contains(@placeholder,'To')]"
                )
            )
        )

        active_input.click()

        time.sleep(1)

        active_input.send_keys(
            Keys.CONTROL + "a"
        )

        active_input.send_keys(
            Keys.DELETE
        )

        time.sleep(1)

        for ch in city:

            active_input.send_keys(ch)

            time.sleep(0.3)

        logger.info(
            f"TYPED CITY: {city}"
        )

        time.sleep(2)

        # FIX: Keyboard navigation forces React to save the state
        active_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        active_input.send_keys(Keys.ENTER)

        logger.info(
            f"SELECTED CITY: {city}"
        )

        time.sleep(2)

    def select_date(self):

        try:

            self.driver.find_element(
                By.TAG_NAME,
                "body"
            ).click()

            time.sleep(1)

            date_box = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        By.ID,
                        "travelDate"
                    )
                )
            )

            # ORIGINAL: JS Click to open the calendar safely
            self.driver.execute_script(
                "arguments[0].click();",
                date_box
            )

            logger.info(
                "DATE BOX CLICKED"
            )

            time.sleep(2)

            available_dates = self.wait.until(
                EC.presence_of_all_elements_located(
                    (
                        By.XPATH,
                        "//div[contains(@class,'DayPicker-Day') and not(contains(@class,'disabled'))]"
                    )
                )
            )

            # FIX: Standard click on date forces React state hook
            available_dates[9].click()

            logger.info(
                "DATE SELECTED"
            )

            time.sleep(2)

        except Exception as e:

            logger.info(
                f"DATE ISSUE: {str(e)}"
            )

            raise

    def click_search(self):

        logger.info(
            "CLICKING SEARCH BUTTON"
        )

        search_btn = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.ID,
                    "search_button"
                )
            )
        )

        # SCROLL TO BUTTON
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            search_btn
        )

        time.sleep(2)

        # REAL USER CLICK
        search_btn.click()

        logger.info(
            "SEARCH BUTTON CLICKED SUCCESSFULLY"
        )

        time.sleep(10)

    def search_bus(self, from_city, to_city):

        logger.info(
            "STARTING BUS SEARCH"
        )

        self.close_popup()

        self.select_bus_tab()

        from_field = (
            By.ID,
            "fromCity"
        )

        to_field = (
            By.ID,
            "toCity"
        )

        logger.info(
            f"FROM CITY: {from_city}"
        )

        self.select_city(
            from_field,
            from_city
        )

        logger.info(
            f"TO CITY: {to_city}"
        )

        self.select_city(
            to_field,
            to_city
        )

        self.select_date()

        self.click_search()

        logger.info(
            "BUS SEARCH COMPLETED"
        )