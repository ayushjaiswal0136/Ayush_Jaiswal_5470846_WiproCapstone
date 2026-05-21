import time
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.seat_locators import SeatLocators
from utils.logger import LogGen

logger = LogGen.loggen()

class SeatPage(BasePage):
    def fill_passenger_details(self, name, age, gender):
        logger.info("POM LOG: INITIALIZING TRAVELLER DETAILS FORM SECTIONS")
        try:
            name_input = self.wait.until(EC.presence_of_element_located(SeatLocators.NAME_FIELD))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_input)
            time.sleep(1)
            name_input.clear()
            name_input.send_keys(name)
            logger.info(f"POM LOG: TRAVELLER NAME COMMITTED -> {name}")

            age_input = self.wait.until(EC.presence_of_element_located(SeatLocators.AGE_FIELD))
            age_input.clear()
            clean_age = str(int(float(age))) if '.' in str(age) else str(age)
            age_input.send_keys(clean_age)
            logger.info(f"POM LOG: TRAVELLER AGE COMMITTED -> {clean_age}")
            time.sleep(1)

            gender_clean = str(gender).strip().lower()
            if "male" in gender_clean and "female" not in gender_clean:
                gender_element = self.wait.until(EC.presence_of_element_located(SeatLocators.MALE_GENDER_TAB))
            else:
                gender_element = self.wait.until(EC.presence_of_element_located(SeatLocators.FEMALE_GENDER_TAB))

            self.driver.execute_script("arguments[0].click();", gender_element)
            logger.info(f"POM LOG: GENDER MATCH SELECTION DEPLOYED -> {gender_clean}")
            time.sleep(1.5)
        except Exception as e:
            logger.error(f"POM LOG: FAIL OCCURRED FILLING PRIMARY TRAVELLER FORM BLOCKS: {str(e)}")
            raise

    def fill_contact_details(self, mobile, email):
        logger.info("POM LOG: INITIALIZING CONTACT DETAILS FORM SECTIONS")
        try:
            email_input = self.wait.until(EC.presence_of_element_located(SeatLocators.EMAIL_FIELD))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", email_input)
            time.sleep(1)
            email_input.clear()
            email_input.send_keys(email)
            logger.info(f"POM LOG: CONTACT EMAIL ADDRESS STRINGS ASSIGNED -> {email}")
            time.sleep(1)

            mobile_input = self.wait.until(EC.presence_of_element_located(SeatLocators.MOBILE_FIELD))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", mobile_input)
            time.sleep(1)
            mobile_input.clear()
            clean_mobile = str(int(float(mobile))) if '.' in str(mobile) else str(mobile)
            mobile_input.send_keys(clean_mobile)
            logger.info(f"POM LOG: CONTACT MOBILE NUMBER STRINGS ASSIGNED -> {clean_mobile}")
            time.sleep(1.5)
        except Exception as e:
            logger.error(f"POM LOG: FAIL OCCURRED FILLING CUSTOMER CONTACT INFORMATION CARDS: {str(e)}")
            raise

    def select_required_options_and_continue(self):
        logger.info("POM LOG: DISPATCHING MANDATORY/OPTIONAL CHECKBOX FORM LAYERS")
        try:
            # 1. OPTIONAL/CONDITIONAL: Handle State Selection first
            try:
                state_dropdown = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(SeatLocators.STATE_DROPDOWN)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", state_dropdown)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", state_dropdown)
                time.sleep(1)

                state_option = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(SeatLocators.STATE_OPTION)
                )
                self.driver.execute_script("arguments[0].click();", state_option)
                logger.info("POM LOG: STATE SELECTION PARSED SUCCESSFULLY")
                time.sleep(1.5)
            except Exception as e:
                logger.info(f"POM LOG: STATE DROPDOWN SKIPPED OR ALREADY FILLED.")

            # 2. CHECKBOX: Billing Details (The one causing the red outline)
            try:
                billing_cb = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(SeatLocators.BILLING_DETAILS_CHECKBOX)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", billing_cb)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", billing_cb)
                logger.info("POM LOG: BILLING SAVE COMPLIANCE CLICKED")
                time.sleep(1)
            except Exception:
                # BRUTE FORCE BACKUP: Find by pure innerText and click its parent
                logger.info("POM LOG: Trying JS brute-force for Billing Checkbox...")
                try:
                    self.driver.execute_script("""
                        var elements = document.evaluate("//*[contains(text(), 'save billing details')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                        if(elements.snapshotLength > 0) { elements.snapshotItem(0).click(); }
                    """)
                    time.sleep(1)
                except:
                    logger.info("POM LOG: BILLING DETAILS CHECKBOX COMPLETELY SKIPPED.")

            # 3. RADIO: TripAssured protection plan
            try:
                trip_no_radio = WebDriverWait(self.driver, 4).until(
                    EC.presence_of_element_located(SeatLocators.TRIP_ASSURED_NO_RADIO)
                )
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", trip_no_radio)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", trip_no_radio)
                logger.info("POM LOG: TRIPASSURED DISMISS SELECTION CLICKED")
                time.sleep(1)
            except Exception:
                logger.info("POM LOG: Trying JS brute-force for TripAssured...")
                try:
                    self.driver.execute_script("""
                        var elements = document.evaluate("//*[contains(text(), 'No') and contains(text(), 'need it')]", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                        if(elements.snapshotLength > 0) { elements.snapshotItem(0).click(); }
                    """)
                    time.sleep(1)
                except:
                    logger.info("POM LOG: TRIP ASSURED OPTION COMPLETELY SKIPPED.")

            # 4. SUBMIT: Target and invoke the Final checkout section submit button
            submit_btn = self.wait.until(
                EC.presence_of_element_located(SeatLocators.BOTTOM_CONTINUE_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
            time.sleep(2)

            # Fire standard direct execution JS click
            self.driver.execute_script("arguments[0].click();", submit_btn)
            logger.info("POM LOG: REVEAL PAYMENT OPTIONS DISPATCH STEP COMPLETE")
            time.sleep(8)

        except Exception as e:
            logger.error(f"POM LOG: PIPELINE CONTEXT BLOCKED ON FINAL CHECKOUT OPERATIONS: {str(e)}")
            raise