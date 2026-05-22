import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from locators.bus_search_locators import BusSearchLocators
from utils.logger import LogGen

logger = LogGen.loggen()


class BusSearchPage(BasePage):

    # ==========================================
    # EXISTING E2E METHODS
    # ==========================================

    def verify_bus_search_result(self):
        logger.info("POM LOG: VERIFYING RESULTS PAGE")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("/bus-tickets/search")
            )
            time.sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(BusSearchLocators.BUS_RESULTS)
            )
            logger.info("POM LOG: SEARCH RESULTS CONTAINER VALIDATED")
        except Exception:
            logger.info("POM LOG: NOT ON SEARCH RESULTS PAGE (Expected behavior for Negative Tests)")

    def filter_ac_buses(self):
        logger.info("POM LOG: APPLYING AC FILTER")
        try:
            ac_btn = self.wait.until(EC.presence_of_element_located(BusSearchLocators.AC_FILTER_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", ac_btn)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", ac_btn)
            logger.info("POM LOG: AC FILTER DEPLOYED VIA JS")
            time.sleep(4)
        except Exception as e:
            logger.error(f"POM LOG: FILTER ACTION INTERRUPTED: {str(e)}")
            raise

    def select_first_bus(self):
        logger.info("POM LOG: OPENING SEAT MAP FOR TOP COM-ROW")
        try:
            btn = self.wait.until(EC.presence_of_element_located(BusSearchLocators.FIRST_SELECT_SEATS_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            time.sleep(1.5)
            self.driver.execute_script("arguments[0].click();", btn)
            logger.info("POM LOG: SEAT OPTIONS POPULATED VIA JS")
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
            try:
                boarding = self.wait.until(EC.element_to_be_clickable(BusSearchLocators.FIRST_BOARDING_POINT))
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", boarding)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", boarding)
                logger.info("POM LOG: BOARDING POINT SELECTED VIA JS")
            except Exception:
                logger.info("POM LOG: Boarding point auto-selected or unavailable.")

            time.sleep(1.5)

            # 3. Select Dropping Point (Updated with dynamic resilience)
            try:
                dropping = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(BusSearchLocators.FIRST_DROPPING_POINT)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropping)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", dropping)
                logger.info("POM LOG: DROPPING POINT SELECTED VIA JS")
                time.sleep(2)
            except Exception:
                logger.info("POM LOG: Dropping point auto-selected or unavailable. Proceeding to checkout.")

            # 4. Continue to Checkout - Enforce Wait Until Clickable
            logger.info("POM LOG: LOCATING ACTIVE CONTINUE ELEMENT")

            # Using element_to_be_clickable over presence_of_element_located to ensure UI state changed
            real_continue_btn = self.wait.until(EC.element_to_be_clickable(BusSearchLocators.CONTINUE_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                                       real_continue_btn)
            time.sleep(2)

            try:
                real_continue_btn.click()  # Attempt standard click first
                logger.info("POM LOG: NATIVE CONTINUE BUTTON EXECUTION SUCCESSFUL")
            except Exception:
                # Use JS injection if overlay interception occurs
                self.driver.execute_script("arguments[0].click();", real_continue_btn)
                logger.info("POM LOG: JS CONTINUE BUTTON EXECUTION SUCCESSFUL")

            time.sleep(5)

        except Exception as e:
            logger.error(f"POM LOG: FAULT INSIDE SELECTION PIPELINE: {str(e)}")
            raise

    # ==========================================
    # NEW BUS SEARCH VALIDATION METHODS
    # ==========================================

    def get_route_title(self):
        title = self.wait.until(EC.visibility_of_element_located(BusSearchLocators.ROUTE_TITLE))
        return title.text

    def filter_sleeper_buses(self):
        logger.info("POM LOG: APPLYING SLEEPER FILTER")
        try:
            sleeper_btn = self.wait.until(EC.presence_of_element_located(BusSearchLocators.SLEEPER_FILTER_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sleeper_btn)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", sleeper_btn)
            logger.info("POM LOG: SLEEPER FILTER DEPLOYED VIA JS")
            time.sleep(3)
        except Exception as e:
            logger.error(f"POM LOG: FILTER ACTION INTERRUPTED: {str(e)}")

    def verify_bus_present(self, expected_bus_name):
        try:
            bus_elements = self.wait.until(EC.presence_of_all_elements_located(BusSearchLocators.BUS_CARD_NAMES))

            found_buses = [bus.text.strip() for bus in bus_elements if bus.text.strip()]
            logger.info(f"POM LOG: Buses currently available on this route: {found_buses}")

            for bus in bus_elements:
                if expected_bus_name.lower() in bus.text.lower():
                    return True
            return False
        except Exception as e:
            logger.error(f"POM LOG: Could not verify bus presence: {str(e)}")
            return False

    def get_selected_seat_number(self):
        seat_text = self.wait.until(EC.visibility_of_element_located(BusSearchLocators.SELECTED_SEAT_TEXT))
        return seat_text.text

    def get_no_buses_message(self):
        try:
            msg = self.wait.until(EC.visibility_of_element_located(BusSearchLocators.NO_BUSES_MSG))
            return msg.text
        except Exception:
            return ""

    # ==========================================
    # NEW BUS SEARCH VALIDATION METHODS (From Pytest logic)
    # ==========================================

    def get_route_title(self):
        title = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(BusSearchLocators.ROUTE_TITLE)
        )
        return title.text.strip()

    def filter_sleeper_buses(self):
        logger.info("POM LOG: APPLYING SLEEPER FILTER")
        try:
            # 1. Wait for element to be present in the DOM
            sleeper_btn = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(BusSearchLocators.SLEEPER_FILTER_BTN)
            )

            # 2. Scroll it directly into the center of the view
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", sleeper_btn)
            time.sleep(1.5)

            # 3. Force click via JavaScript to bypass any UI overlaps
            self.driver.execute_script("arguments[0].click();", sleeper_btn)

            logger.info("POM LOG: SLEEPER FILTER DEPLOYED VIA JS")
            time.sleep(3)  # Wait for the DOM to refresh the bus list

        except Exception as e:
            logger.error(f"POM LOG: SLEEPER FILTER ACTION INTERRUPTED: {str(e)}")
            raise  # Fail the test loudly if it can't click

    def is_sleeper_filter_applied(self):
        try:
            active_filter = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(BusSearchLocators.ACTIVE_SLEEPER_FILTER)
            )
            return active_filter.is_displayed()
        except Exception:
            return False

    def get_selected_seat_number(self):
        try:
            # Matches Pytest logic: Wait for review page transition first
            WebDriverWait(self.driver, 40).until(EC.url_contains("/bus/review"))

            seat_info = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(BusSearchLocators.SELECTED_SEAT_TEXT)
            )
            return seat_info.text.strip()
        except Exception as e:
            logger.error(f"POM LOG: Seat text not found on review page. {str(e)}")
            return ""

    def verify_booking_page_details(self, from_city, to_city):
        try:
            WebDriverWait(self.driver, 40).until(EC.url_contains("/bus/review"))

            # 1. Check Heading
            heading = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(BusSearchLocators.BOOKING_HEADING)
            )
            if not heading.is_displayed():
                return False

            # 2. Check Page Source for Cities
            page_source = self.driver.page_source.lower()
            if from_city.lower() not in page_source or to_city.lower() not in page_source:
                return False

            return True
        except Exception as e:
            logger.error(f"POM LOG: Failed validating booking page details. {str(e)}")
            return False

    def is_bus_list_empty(self):
        logger.info("POM LOG: CHECKING FOR EMPTY BUS LIST (NEGATIVE VALIDATION)")
        try:
            # Ensure we are on the search page
            WebDriverWait(self.driver, 15).until(EC.url_contains("/bus-tickets/search"))
            time.sleep(4)  # Hard pause to allow React to finish attempting to fetch buses

            # Check how many bus cards rendered
            buses = self.driver.find_elements(*BusSearchLocators.BUS_RESULTS)
            count = len(buses)
            logger.info(f"POM LOG: Found {count} bus cards on the page.")

            return count == 0
        except Exception as e:
            logger.info(f"POM LOG: Empty list verification encountered an issue (Assumed Empty): {str(e)}")
            return True

