from selenium.webdriver.common.by import By

class HomeLocators:
    CLOSE_MODAL = (By.XPATH, "//span[@data-cy='closeModal']")
    BODY = (By.TAG_NAME, "body")
    BUS_TAB = (By.XPATH, "//span[contains(text(),'Buses')]")
    FROM_CITY_FIELD = (By.ID, "fromCity")
    TO_CITY_FIELD = (By.ID, "toCity")
    ACTIVE_INPUT = (By.XPATH, "//input[contains(@placeholder,'From') or contains(@placeholder,'To')]")
    TRAVEL_DATE_BOX = (By.ID, "travelDate")
    AVAILABLE_DATES = (By.XPATH, "//div[contains(@class,'DayPicker-Day') and not(contains(@class,'disabled'))]")
    SEARCH_BTN = (By.ID, "search_button")