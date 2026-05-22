import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.home_locators import HomeLocators
from utils.logger import LogGen

logger = LogGen.loggen()

class HomePage(BasePage):
    def close_popup(self):
        try:
            time.sleep(2)
            close_btn = self.driver.find_element(*HomeLocators.CLOSE_MODAL)
            self.driver.execute_script("arguments[0].click();", close_btn)
            logger.info("LOGIN POPUP CLOSED")
            time.sleep(1)
        except:
            try:
                body = self.driver.find_element(*HomeLocators.BODY)
                body.click()
                logger.info("CLICKED OUTSIDE POPUP")
                time.sleep(1)
            except:
                logger.info("NO POPUP FOUND")

    def select_bus_tab(self):
        try:
            bus_tab = self.wait.until(EC.element_to_be_clickable(HomeLocators.BUS_TAB))
            self.driver.execute_script("arguments[0].click();", bus_tab)
            logger.info("BUS TAB CLICKED")
            time.sleep(2)
        except Exception as e:
            logger.info(f"BUS TAB ISSUE: {str(e)}")

    def select_city(self, field_locator, city):
        city_box = self.wait.until(EC.element_to_be_clickable(field_locator))
        self.driver.execute_script("arguments[0].click();", city_box)
        logger.info(f"CLICKED FIELD: {city}")
        time.sleep(2)

        active_input = self.wait.until(EC.visibility_of_element_located(HomeLocators.ACTIVE_INPUT))
        active_input.click()
        time.sleep(1)
        active_input.send_keys(Keys.CONTROL + "a")
        active_input.send_keys(Keys.DELETE)
        time.sleep(1)

        for ch in city:
            active_input.send_keys(ch)
            time.sleep(0.3)

        logger.info(f"TYPED CITY: {city}")
        time.sleep(2)
        active_input.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        active_input.send_keys(Keys.ENTER)
        logger.info(f"SELECTED CITY: {city}")
        time.sleep(2)

    def select_date(self):
        try:
            self.driver.find_element(*HomeLocators.BODY).click()
            time.sleep(1)
            date_box = self.wait.until(EC.element_to_be_clickable(HomeLocators.TRAVEL_DATE_BOX))
            self.driver.execute_script("arguments[0].click();", date_box)
            logger.info("DATE BOX CLICKED")
            time.sleep(2)

            available_dates = self.wait.until(EC.presence_of_all_elements_located(HomeLocators.AVAILABLE_DATES))
            available_dates[7].click()
            logger.info("DATE SELECTED")
            time.sleep(2)
        except Exception as e:
            logger.info(f"DATE ISSUE: {str(e)}")
            raise

    def click_search(self):
        logger.info("CLICKING SEARCH BUTTON")
        search_btn = self.wait.until(EC.element_to_be_clickable(HomeLocators.SEARCH_BTN))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", search_btn)
        time.sleep(2)
        search_btn.click()
        logger.info("SEARCH BUTTON CLICKED SUCCESSFULLY")
        time.sleep(10)

    def search_bus(self, from_city, to_city):
        logger.info("STARTING BUS SEARCH")
        self.close_popup()
        self.select_bus_tab()
        logger.info(f"FROM CITY: {from_city}")
        self.select_city(HomeLocators.FROM_CITY_FIELD, from_city)
        logger.info(f"TO CITY: {to_city}")
        self.select_city(HomeLocators.TO_CITY_FIELD, to_city)
        self.select_date()
        self.click_search()
        logger.info("BUS SEARCH COMPLETED")

    # NEW: Added method to extract same city error text for Negative Search Scenarios
    def get_same_city_error(self):
        try:
            error_element = self.wait.until(EC.visibility_of_element_located(HomeLocators.SAME_CITY_ERROR))
            logger.info(f"POM LOG: SAME CITY ERROR DETECTED -> {error_element.text}")
            return error_element.text
        except Exception as e:
            logger.info(f"POM LOG: SAME CITY ERROR NOT FOUND. {str(e)}")
            return ""