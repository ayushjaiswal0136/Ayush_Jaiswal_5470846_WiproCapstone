import time
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.payment_locators import PaymentLocators
from utils.logger import LogGen

logger = LogGen.loggen()

class PaymentPage(BasePage):
    def select_credit_card_option(self):
        logger.info("POM LOG: LOCATING CREDIT/DEBIT CARD PAYMENT TAB")
        try:
            time.sleep(5)
            cc_tab = self.wait.until(EC.presence_of_element_located(PaymentLocators.CREDIT_CARD_TAB))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", cc_tab)
            time.sleep(1)
            fresh_cc_tab = self.driver.find_element(*PaymentLocators.CREDIT_CARD_TAB)
            self.driver.execute_script("arguments[0].click();", fresh_cc_tab)
            logger.info("POM LOG: CREDIT/DEBIT CARD TAB SELECTED SUCCESSFULLY")
            time.sleep(2)
        except Exception as e:
            logger.error(f"POM LOG: FAILED TO LOCATE OR CLICK CREDIT CARD TAB: {str(e)}")
            raise

    def enter_card_details(self, card_number, expiry, cvv, card_holder):
        logger.info("POM LOG: INITIALIZING CARD DETAILS INJECTION")
        try:
            card_input = self.wait.until(EC.presence_of_element_located(PaymentLocators.CARD_NUMBER_FIELD))
            card_input.clear()
            clean_card = str(int(float(card_number))) if '.' in str(card_number) else str(card_number)
            card_input.send_keys(clean_card)
            logger.info("POM LOG: CARD NUMBER COMMITTED")
            time.sleep(1)

            month, year = "12", "28"
            if "/" in str(expiry):
                month, year = str(expiry).split("/")

            mm_input = self.wait.until(EC.presence_of_element_located(PaymentLocators.EXPIRY_MM_FIELD))
            try:
                mm_input.clear()
                mm_input.send_keys(month.strip())
            except Exception:
                self.driver.execute_script("arguments[0].click();", mm_input)
                time.sleep(1)
                month_opt = self.driver.find_element(By.XPATH, f"//li[text()='{month.strip()}'] | //span[text()='{month.strip()}']")
                self.driver.execute_script("arguments[0].click();", month_opt)
            logger.info(f"POM LOG: EXPIRY MONTH COMMITTED -> {month.strip()}")
            time.sleep(0.5)

            yy_input = self.wait.until(EC.presence_of_element_located(PaymentLocators.EXPIRY_YY_FIELD))
            try:
                yy_input.clear()
                yy_input.send_keys(year.strip())
            except Exception:
                self.driver.execute_script("arguments[0].click();", yy_input)
                time.sleep(1)
                year_opt = self.driver.find_element(By.XPATH, f"//li[text()='{year.strip()}'] | //span[text()='{year.strip()}']")
                self.driver.execute_script("arguments[0].click();", year_opt)
            logger.info(f"POM LOG: EXPIRY YEAR COMMITTED -> {year.strip()}")
            time.sleep(0.5)

            cvv_input = self.wait.until(EC.presence_of_element_located(PaymentLocators.CVV_FIELD))
            cvv_input.clear()
            clean_cvv = str(int(float(cvv))) if '.' in str(cvv) else str(cvv)
            cvv_input.send_keys(clean_cvv)
            logger.info("POM LOG: CVV COMMITTED")
            time.sleep(0.5)

            try:
                name_input = self.driver.find_element(*PaymentLocators.NAME_ON_CARD_FIELD)
                name_input.clear()
                name_input.send_keys(str(card_holder))
                logger.info("POM LOG: CARD HOLDER NAME COMMITTED")
                time.sleep(1)
            except Exception:
                logger.info("POM LOG: CARD HOLDER NAME FIELD NOT PRESENT/REQUIRED ON THIS VIEW. SKIPPING.")

            logger.info("POM LOG: ALL DUMMY PAYMENT DETAILS INJECTED SUCCESSFULLY. END OF E2E FLOW REACHED.")
            time.sleep(3)
        except Exception as e:
            logger.error(f"POM LOG: FAULT OCCURRED WHILE INJECTING CARD DATA: {str(e)}")
            raise