import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class BusSearchPage(BasePage):
    # CORE DOM COMPONENT LOCATORS
    BUS_RESULTS = (By.CSS_SELECTOR, "div[class*='BusCard_listingCard'], div[id^='listing-bus-card']")
    AC_FILTER_BTN = (By.CSS_SELECTOR, "ul[class*='FilterTabs_tabCtr'] div[class*='FilterTabs_tabSection']")
    FIRST_SELECT_SEATS_BTN = (By.CSS_SELECTOR,
                              "div[id^='listing-bus-card'] button[class*='button'], div[id^='listing-bus-card'] button")

    AVAILABLE_SEAT = (By.CSS_SELECTOR, "div[class*='Tooltip_tooltipWrapper'] img[alt='SEATER']")

    # ADDED: Plural locator to grab ALL available seat icons for the loop
    AVAILABLE_SEATS = (By.CSS_SELECTOR,
                       "div[class*='Tooltip_tooltipWrapper'] img[alt='SEATER'], div[class*='Tooltip_tooltipWrapper'] img[alt='SLEEPER']")

    FIRST_BOARDING_POINT = (By.XPATH, "(//label[contains(@class,'PickUpDropSelection_pickDropItem')])[1]")
    FIRST_DROPPING_POINT = (By.XPATH, "(//label[contains(@class,'PickUpDropSelection_pickDropItem')])[4]")

    # THE ABSOLUTE CORRECT TARGET: Lock onto the active button container nested uniquely within the selection panel block wrapper
    CONTINUE_BTN = (By.XPATH,
                    "//div[contains(@class, 'PickUpDropSelection_bottomSectionContainer')]//button[contains(@class, 'Button_primary')] | //button[contains(@class,'Button_primary') and text()='CONTINUE']")

    def verify_bus_search_result(self):
        logger.info("POM LOG: VERIFYING RESULTS PAGE")
        WebDriverWait(self.driver, 60).until(
            EC.url_contains("/bus-tickets/search")
        )
        time.sleep(3)
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located(self.BUS_RESULTS)
        )
        logger.info("POM LOG: SEARCH RESULTS CONTAINER VALIDATED")

    def filter_ac_buses(self):
        logger.info("POM LOG: APPLYING AC FILTER")
        try:
            ac_btn = WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable(self.AC_FILTER_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ac_btn)
            time.sleep(1.5)
            ac_btn.click()
            logger.info("POM LOG: AC FILTER DEPLOYED NATIVELY")
            time.sleep(4)
        except Exception as e:
            logger.error(f"POM LOG: FILTER ACTION INTERRUPTED: {str(e)}")
            raise

    def select_first_bus(self):
        logger.info("POM LOG: OPENING SEAT MAP FOR TOP COM-ROW")
        try:
            btn = WebDriverWait(self.driver, 25).until(
                EC.element_to_be_clickable(self.FIRST_SELECT_SEATS_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(1.5)
            btn.click()
            logger.info("POM LOG: SEAT OPTIONS POPULATED NATIVELY")
            time.sleep(3)
        except Exception as e:
            logger.error(f"CARD EXPANSION FAILED: {str(e)}")
            raise

    def select_seat_and_points_and_continue(self):
        logger.info("POM LOG: SELECTING SEAT, BOARDING, AND DROPPING POINTS")
        try:
            # 1. DYNAMIC VACANT SEAT FINDER (Replaced the single static click)
            logger.info("POM LOG: SEARCHING FOR ANY AVAILABLE VACANT SEAT")
            seats = WebDriverWait(self.driver, 25).until(
                EC.presence_of_all_elements_located(self.AVAILABLE_SEATS)
            )

            seat_selected = False
            for index, seat in enumerate(seats):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", seat)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", seat)
                    time.sleep(1.5)

                    # Verification check: If the seat is truly vacant and selected, the boarding point will appear
                    WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable(self.FIRST_BOARDING_POINT)
                    )
                    seat_selected = True
                    logger.info(f"POM LOG: VACANT SEAT AT INDEX {index} SUCCESSFULLY SELECTED")
                    break  # Break out of the loop because we got our seat!

                except Exception:
                    logger.info(f"POM LOG: Seat at index {index} is occupied or blocked. Trying next...")
                    continue  # Move to the next iteration in the loop

            if not seat_selected:
                raise Exception("Iterated through all visible seats but could not lock in any vacant one.")

            # 2. Select Boarding Point
            boarding = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.FIRST_BOARDING_POINT)
            )
            boarding.click()
            logger.info("POM LOG: BOARDING POINT SELECTED NATIVELY")
            time.sleep(1.5)

            # 3. Select Dropping Point
            dropping = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.FIRST_DROPPING_POINT)
            )
            dropping.click()
            logger.info("POM LOG: DROPPING POINT SELECTED NATIVELY")
            time.sleep(2)

            # 4. Target and center the absolute active form button
            logger.info("POM LOG: LOCATING ACTIVE CONTINUE ELEMENT")
            real_continue_btn = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(self.CONTINUE_BTN)
            )

            # Center the element perfectly in the viewport
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                                       real_continue_btn)
            time.sleep(2)

            # Fire the click via direct JavaScript to dispatch form submission safely
            self.driver.execute_script("arguments[0].click();", real_continue_btn)
            logger.info("POM LOG: ACTIVE CONTINUE BUTTON EXECUTION SUCCESSFUL")
            time.sleep(5)

        except Exception as e:
            logger.error(f"POM LOG: FAULT INSIDE SELECTION PIPELINE: {str(e)}")
            raise