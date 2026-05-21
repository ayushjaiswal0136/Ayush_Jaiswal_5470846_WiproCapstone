import time
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.bus_search_locators import BusSearchLocators
from utils.logger import LogGen

logger = LogGen.loggen()


class BusSearchPage(BasePage):
    def verify_bus_search_result(self):
        logger.info("POM LOG: VERIFYING RESULTS PAGE")
        self.wait.until(EC.url_contains("/bus-tickets/search"))
        time.sleep(3)
        self.wait.until(EC.presence_of_element_located(BusSearchLocators.BUS_RESULTS))
        logger.info("POM LOG: SEARCH RESULTS CONTAINER VALIDATED")

    def filter_ac_buses(self):
        logger.info("POM LOG: APPLYING AC FILTER")
        try:
            ac_btn = self.wait.until(EC.element_to_be_clickable(BusSearchLocators.AC_FILTER_BTN))
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
            btn = self.wait.until(EC.element_to_be_clickable(BusSearchLocators.FIRST_SELECT_SEATS_BTN))
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
            logger.info("POM LOG: SEARCHING FOR ANY AVAILABLE VACANT SEAT")
            seats = self.wait.until(EC.presence_of_all_elements_located(BusSearchLocators.AVAILABLE_SEATS))

            seat_selected = False
            for index, seat in enumerate(seats):
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", seat)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", seat)
                    time.sleep(1.5)
                    self.wait.until(EC.element_to_be_clickable(BusSearchLocators.FIRST_BOARDING_POINT))
                    seat_selected = True
                    logger.info(f"POM LOG: VACANT SEAT AT INDEX {index} SUCCESSFULLY SELECTED")
                    break
                except Exception:
                    logger.info(f"POM LOG: Seat at index {index} is occupied or blocked. Trying next...")
                    continue

            if not seat_selected:
                raise Exception("Iterated through all visible seats but could not lock in any vacant one.")

            # 2. Select Boarding Point
            boarding = self.wait.until(EC.element_to_be_clickable(BusSearchLocators.FIRST_BOARDING_POINT))
            boarding.click()
            logger.info("POM LOG: BOARDING POINT SELECTED NATIVELY")
            time.sleep(1.5)

            # 3. Select Dropping Point (Updated with dynamic resilience)
            try:
                # First, try the original locator
                dropping = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(BusSearchLocators.FIRST_DROPPING_POINT)
                )
                dropping.click()
                logger.info("POM LOG: DROPPING POINT SELECTED (INDEX 4)")
                time.sleep(2)
            except Exception:
                logger.info("POM LOG: Index 4 not found. Trying dynamic alternative for Dropping Point.")
                try:
                    # Fallback: Click the very last available pickup/drop item in the DOM list
                    from selenium.webdriver.common.by import By
                    fallback_locator = (By.XPATH,
                                        "(//label[contains(@class,'PickUpDropSelection_pickDropItem')])[last()]")
                    dropping_fallback = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(fallback_locator)
                    )
                    dropping_fallback.click()
                    logger.info("POM LOG: DROPPING POINT SELECTED VIA FALLBACK")
                    time.sleep(2)
                except Exception:
                    # If it still fails, MMT likely auto-selected it (happens if only 1 drop point exists)
                    logger.info("POM LOG: Dropping point auto-selected or unavailable. Proceeding to checkout.")

            # 4. Continue to Checkout
            logger.info("POM LOG: LOCATING ACTIVE CONTINUE ELEMENT")
            real_continue_btn = self.wait.until(EC.presence_of_element_located(BusSearchLocators.CONTINUE_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                                       real_continue_btn)
            time.sleep(2)
            self.driver.execute_script("arguments[0].click();", real_continue_btn)
            logger.info("POM LOG: ACTIVE CONTINUE BUTTON EXECUTION SUCCESSFUL")
            time.sleep(5)

        except Exception as e:
            logger.error(f"POM LOG: FAULT INSIDE SELECTION PIPELINE: {str(e)}")
            raise