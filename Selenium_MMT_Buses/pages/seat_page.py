# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from pages.base_page import BasePage
# from utils.logger import LogGen
#
# logger = LogGen.loggen()
#
#
# class SeatPage(BasePage):
#     # DETAILED PASSENGER FORM FIELD TARGET LOCATORS
#     NAME_FIELD = (By.CSS_SELECTOR,
#                   "input[placeholder='Type here'], div[class*='confirmFormWrapper'] input[type='text']")
#     AGE_FIELD = (By.CSS_SELECTOR, "input[placeholder='eg: 24'], input[id='age']")
#
#     MALE_GENDER_TAB = (By.CSS_SELECTOR, "div.maleTab, div[class*='maleTab'], .maleTab")
#     FEMALE_GENDER_TAB = (By.CSS_SELECTOR, "div.femaleTab, div[class*='femaleTab'], .femaleTab")
#
#     EMAIL_FIELD = (By.CSS_SELECTOR, "input[id='emailId'], input[type='email']")
#
#     # FIXED LOCATOR: Added direct resilient XPATH mapping for mobile phone components
#     MOBILE_FIELD = (By.XPATH, "//input[@id='contactMobile'] | //input[@type='tel'] | //input[contains(@id,'mobile')]")
#
#     BILLING_DETAILS_CHECKBOX = (By.XPATH,
#                                 "//p[contains(text(),'Confirm and save billing details')]/preceding-sibling::span | //p[contains(text(),'Confirm and save billing details')] | //span[contains(@class,'checkboxWp')]")
#     TRIP_ASSURED_NO_RADIO = (By.XPATH,
#                              "//span[contains(text(),\"No,I don't need it\")] | //span[text()=\"No,I don't need it\"] | //span[contains(@class,'appendLeft10') and contains(text(),'No')]")
#
#     BOTTOM_CONTINUE_BTN = (By.CSS_SELECTOR,
#                            "div[class*='paymentBtn'] span, div.paymentBtn, .paymentBtn, button[class*='paymentBtn']")
#
#     def fill_passenger_details(self, name, age, gender, mobile, email):
#         logger.info("POM LOG: INITIALIZING TRAVELLER DETAILS FORM SECTIONS")
#         try:
#             # 1. Provide Traveller Full Name
#             name_input = WebDriverWait(self.driver, 25).until(
#                 EC.presence_of_element_located(self.NAME_FIELD)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", name_input)
#             time.sleep(1)
#             name_input.clear()
#             name_input.send_keys(name)
#             logger.info(f"POM LOG: TRAVELLER NAME COMMITTED -> {name}")
#
#             # 2. Provide Traveller Age
#             age_input = WebDriverWait(self.driver, 20).until(
#                 EC.presence_of_element_located(self.AGE_FIELD)
#             )
#             age_input.clear()
#             clean_age = str(int(float(age))) if '.' in str(age) else str(age)
#             age_input.send_keys(clean_age)
#             logger.info(f"POM LOG: TRAVELLER AGE COMMITTED -> {clean_age}")
#             time.sleep(1)
#
#             # 3. Handle Dynamic Gender Tab Click Options
#             gender_clean = str(gender).strip().lower()
#             if "male" in gender_clean and "female" not in gender_clean:
#                 gender_element = WebDriverWait(self.driver, 25).until(
#                     EC.presence_of_element_located(self.MALE_GENDER_TAB))
#             else:
#                 gender_element = WebDriverWait(self.driver, 25).until(
#                     EC.presence_of_element_located(self.FEMALE_GENDER_TAB))
#
#             self.driver.execute_script("arguments[0].click();", gender_element)
#             logger.info(f"POM LOG: GENDER MATCH SELECTION DEPLOYED -> {gender_clean}")
#             time.sleep(1.5)
#
#         except Exception as e:
#             logger.error(f"POM LOG: FAIL OCCURRED FILLING PRIMARY TRAVELLER FORM BLOCKS: {str(e)}")
#             raise
#
#     def fill_contact_details(self, mobile, email):
#         logger.info("POM LOG: INITIALIZING CONTACT DETAILS FORM SECTIONS")
#         try:
#             # 1. Handle Email Id Registration Input
#             email_input = WebDriverWait(self.driver, 25).until(
#                 EC.presence_of_element_located(self.EMAIL_FIELD)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", email_input)
#             time.sleep(1)
#             email_input.clear()
#             email_input.send_keys(email)
#             logger.info(f"POM LOG: CONTACT EMAIL ADDRESS STRINGS ASSIGNED -> {email}")
#             time.sleep(1)
#
#             # 2. Handle Mobile Number Registration Input
#             mobile_input = WebDriverWait(self.driver, 25).until(
#                 EC.presence_of_element_located(self.MOBILE_FIELD)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", mobile_input)
#             time.sleep(1)
#             mobile_input.clear()
#             clean_mobile = str(int(float(mobile))) if '.' in str(mobile) else str(mobile)
#             mobile_input.send_keys(clean_mobile)
#             logger.info(f"POM LOG: CONTACT MOBILE NUMBER STRINGS ASSIGNED -> {clean_mobile}")
#             time.sleep(1.5)
#
#         except Exception as e:
#             logger.error(f"POM LOG: FAIL OCCURRED FILLING CUSTOMER CONTACT INFORMATION CARDS: {str(e)}")
#             raise
#
#     def select_required_options_and_continue(self):
#         logger.info("POM LOG: DISPATCHING MANDATORY EXPLICIT CHECKBOX FORM LAYERS")
#         try:
#             # 1. Select the Billing details checkbox option
#             billing_cb = WebDriverWait(self.driver, 25).until(
#                 EC.presence_of_element_located(self.BILLING_DETAILS_CHECKBOX)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", billing_cb)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", billing_cb)
#             logger.info("POM LOG: BILLING SAVE COMPLIANCE PARSED SUCCESSFULLY")
#             time.sleep(1.5)
#
#             # 2. Select TripAssured protection plan radio option
#             trip_no_radio = WebDriverWait(self.driver, 25).until(
#                 EC.presence_of_element_located(self.TRIP_ASSURED_NO_RADIO)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", trip_no_radio)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", trip_no_radio)
#             logger.info("POM LOG: TRIPASSURED DISMISS SELECTION PARSED SUCCESSFULLY")
#             time.sleep(1.5)
#
#             # 3. Target and invoke the Final checkout section submit button element node
#             submit_btn = WebDriverWait(self.driver, 25).until(
#                 EC.presence_of_element_located(self.BOTTOM_CONTINUE_BTN)
#             )
#             self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
#             time.sleep(2)
#
#             # Fire standard direct execution JS click to push clean past any sticking layer frames
#             self.driver.execute_script("arguments[0].click();", submit_btn)
#             logger.info("POM LOG: REVEAL PAYMENT OPTIONS DISPATCH STEP COMPLETE")
#             time.sleep(5)
#
#         except Exception as e:
#             logger.error(f"POM LOG: PIPELINE CONTEXT BLOCKED ON FINALIZE CHECKBOX OPERATIONS: {str(e)}")
#             raise

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.logger import LogGen
from conftest import attach_screenshot

logger = LogGen.loggen()


class SeatPage(BasePage):

    # DETAILED PASSENGER FORM FIELD TARGET LOCATORS
    NAME_FIELD = (
        By.CSS_SELECTOR,
        "input[placeholder='Type here'], div[class*='confirmFormWrapper'] input[type='text']"
    )

    AGE_FIELD = (
        By.CSS_SELECTOR,
        "input[placeholder='eg: 24'], input[id='age']"
    )

    MALE_GENDER_TAB = (
        By.CSS_SELECTOR,
        "div.maleTab, div[class*='maleTab'], .maleTab"
    )

    FEMALE_GENDER_TAB = (
        By.CSS_SELECTOR,
        "div.femaleTab, div[class*='femaleTab'], .femaleTab"
    )

    EMAIL_FIELD = (
        By.CSS_SELECTOR,
        "input[id='emailId'], input[type='email']"
    )

    MOBILE_FIELD = (
        By.XPATH,
        "//input[@id='contactMobile'] | //input[@type='tel'] | //input[contains(@id,'mobile')]"
    )

    BILLING_DETAILS_CHECKBOX = (
        By.XPATH,
        "//p[contains(text(),'Confirm and save billing details')]/preceding-sibling::span | //p[contains(text(),'Confirm and save billing details')] | //span[contains(@class,'checkboxWp')]"
    )

    TRIP_ASSURED_NO_RADIO = (
        By.XPATH,
        "//span[contains(text(),\"No,I don't need it\")] | //span[text()=\"No,I don't need it\"] | //span[contains(@class,'appendLeft10') and contains(text(),'No')]"
    )

    BOTTOM_CONTINUE_BTN = (
        By.CSS_SELECTOR,
        "div[class*='paymentBtn'] span, div.paymentBtn, .paymentBtn, button[class*='paymentBtn']"
    )

    def fill_passenger_details(self, name, age, gender, mobile, email):

        logger.info(
            "POM LOG: INITIALIZING TRAVELLER DETAILS FORM SECTIONS"
        )

        try:

            # 1. Provide Traveller Full Name
            name_input = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(self.NAME_FIELD)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                name_input
            )

            time.sleep(1)

            name_input.clear()

            name_input.send_keys(name)

            logger.info(
                f"POM LOG: TRAVELLER NAME COMMITTED -> {name}"
            )

            attach_screenshot(
                self.driver,
                "Traveller_Name_Entered"
            )

            # 2. Provide Traveller Age
            age_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.AGE_FIELD)
            )

            age_input.clear()

            clean_age = str(int(float(age))) if '.' in str(age) else str(age)

            age_input.send_keys(clean_age)

            logger.info(
                f"POM LOG: TRAVELLER AGE COMMITTED -> {clean_age}"
            )

            attach_screenshot(
                self.driver,
                "Traveller_Age_Entered"
            )

            time.sleep(1)

            # 3. Handle Dynamic Gender Tab Click Options
            gender_clean = str(gender).strip().lower()

            if "male" in gender_clean and "female" not in gender_clean:

                gender_element = WebDriverWait(self.driver, 25).until(
                    EC.presence_of_element_located(
                        self.MALE_GENDER_TAB
                    )
                )

            else:

                gender_element = WebDriverWait(self.driver, 25).until(
                    EC.presence_of_element_located(
                        self.FEMALE_GENDER_TAB
                    )
                )

            self.driver.execute_script(
                "arguments[0].click();",
                gender_element
            )

            logger.info(
                f"POM LOG: GENDER MATCH SELECTION DEPLOYED -> {gender_clean}"
            )

            attach_screenshot(
                self.driver,
                "Gender_Selected"
            )

            time.sleep(1.5)

        except Exception as e:

            logger.error(
                f"POM LOG: FAIL OCCURRED FILLING PRIMARY TRAVELLER FORM BLOCKS: {str(e)}"
            )

            raise

    def fill_contact_details(self, mobile, email):

        logger.info(
            "POM LOG: INITIALIZING CONTACT DETAILS FORM SECTIONS"
        )

        try:

            # 1. Handle Email Id Registration Input
            email_input = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(self.EMAIL_FIELD)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                email_input
            )

            time.sleep(1)

            email_input.clear()

            email_input.send_keys(email)

            logger.info(
                f"POM LOG: CONTACT EMAIL ADDRESS STRINGS ASSIGNED -> {email}"
            )

            attach_screenshot(
                self.driver,
                "Email_Entered"
            )

            time.sleep(1)

            # 2. Handle Mobile Number Registration Input
            mobile_input = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(self.MOBILE_FIELD)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                mobile_input
            )

            time.sleep(1)

            mobile_input.clear()

            clean_mobile = str(int(float(mobile))) if '.' in str(mobile) else str(mobile)

            mobile_input.send_keys(clean_mobile)

            logger.info(
                f"POM LOG: CONTACT MOBILE NUMBER STRINGS ASSIGNED -> {clean_mobile}"
            )

            attach_screenshot(
                self.driver,
                "Mobile_Number_Entered"
            )

            time.sleep(1.5)

        except Exception as e:

            logger.error(
                f"POM LOG: FAIL OCCURRED FILLING CUSTOMER CONTACT INFORMATION CARDS: {str(e)}"
            )

            raise

    def select_required_options_and_continue(self):

        logger.info(
            "POM LOG: DISPATCHING MANDATORY EXPLICIT CHECKBOX FORM LAYERS"
        )

        try:

            # 1. Select Billing Details Checkbox
            billing_cb = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(
                    self.BILLING_DETAILS_CHECKBOX
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                billing_cb
            )

            time.sleep(1)

            self.driver.execute_script(
                "arguments[0].click();",
                billing_cb
            )

            logger.info(
                "POM LOG: BILLING SAVE COMPLIANCE PARSED SUCCESSFULLY"
            )

            attach_screenshot(
                self.driver,
                "Billing_Checkbox_Selected"
            )

            time.sleep(1.5)

            # 2. Select Trip Assured No Radio
            trip_no_radio = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(
                    self.TRIP_ASSURED_NO_RADIO
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                trip_no_radio
            )

            time.sleep(1)

            self.driver.execute_script(
                "arguments[0].click();",
                trip_no_radio
            )

            logger.info(
                "POM LOG: TRIPASSURED DISMISS SELECTION PARSED SUCCESSFULLY"
            )

            attach_screenshot(
                self.driver,
                "Trip_Assured_Disabled"
            )

            time.sleep(1.5)

            # 3. Continue Button
            submit_btn = WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located(
                    self.BOTTOM_CONTINUE_BTN
                )
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                submit_btn
            )

            time.sleep(2)

            self.driver.execute_script(
                "arguments[0].click();",
                submit_btn
            )

            logger.info(
                "POM LOG: REVEAL PAYMENT OPTIONS DISPATCH STEP COMPLETE"
            )

            attach_screenshot(
                self.driver,
                "Continue_To_Payment_Clicked"
            )

            time.sleep(5)

        except Exception as e:

            logger.error(
                f"POM LOG: PIPELINE CONTEXT BLOCKED ON FINALIZE CHECKBOX OPERATIONS: {str(e)}"
            )

            raise