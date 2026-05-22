from selenium.webdriver.common.by import By


class SeatLocators:
    NAME_FIELD = (
        By.CSS_SELECTOR, "input[placeholder='Type here'], div[class*='confirmFormWrapper'] input[type='text']"
    )
    AGE_FIELD = (
        By.CSS_SELECTOR, "input[placeholder='eg: 24'], input[id='age']"
    )
    MALE_GENDER_TAB = (
        By.CSS_SELECTOR, "div.maleTab, div[class*='maleTab'], .maleTab"
    )
    FEMALE_GENDER_TAB = (
        By.CSS_SELECTOR, "div.femaleTab, div[class*='femaleTab'], .femaleTab"
    )
    EMAIL_FIELD = (
        By.CSS_SELECTOR, "input[id='emailId'], input[type='email']"
    )
    MOBILE_FIELD = (
        By.XPATH, "//input[@id='contactMobile'] | //input[@type='tel'] | //input[contains(@id,'mobile')]"
    )

    # UPDATED: Aggressive locators for the tricky checkboxes
    BILLING_DETAILS_CHECKBOX = (
        By.XPATH, "//*[contains(text(), 'save billing details')]/parent::* | //label[contains(.,'Confirm and save billing details')] | //*[contains(text(), 'save billing details')]/preceding-sibling::span"
    )
    TRIP_ASSURED_NO_RADIO = (
        By.XPATH, "//*[contains(text(), 'No') and contains(text(), 'need it')]/parent::* | //span[contains(text(), \"No,I don't need it\")] | //*[contains(text(), 'Add TripAssured')]/../../following-sibling::div//label"
    )

    BOTTOM_CONTINUE_BTN = (
        By.CSS_SELECTOR, "div[class*='paymentBtn'] span, div.paymentBtn, .paymentBtn, button[class*='paymentBtn']"
    )
    STATE_DROPDOWN = (
        By.XPATH, "//*[contains(text(), 'Select the State')]/following::div[1] | //div[contains(@class,'selectState')] | //p[contains(text(), 'State')]/following::div[1]"
    )
    STATE_OPTION = (
        By.XPATH, "//*[text()='Uttar Pradesh'] | //li[contains(text(),'Uttar Pradesh')] | //span[contains(text(),'Uttar Pradesh')]"
    )