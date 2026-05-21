from selenium.webdriver.common.by import By

class BusSearchLocators:
    BUS_RESULTS = (By.CSS_SELECTOR, "div[class*='BusCard_listingCard'], div[id^='listing-bus-card']")
    AC_FILTER_BTN = (By.CSS_SELECTOR, "ul[class*='FilterTabs_tabCtr'] div[class*='FilterTabs_tabSection']")
    FIRST_SELECT_SEATS_BTN = (By.CSS_SELECTOR, "div[id^='listing-bus-card'] button[class*='button'], div[id^='listing-bus-card'] button")
    AVAILABLE_SEATS = (By.CSS_SELECTOR, "div[class*='Tooltip_tooltipWrapper'] img[alt='SEATER'], div[class*='Tooltip_tooltipWrapper'] img[alt='SLEEPER']")
    FIRST_BOARDING_POINT = (By.XPATH, "(//label[contains(@class,'PickUpDropSelection_pickDropItem')])[1]")
    FIRST_DROPPING_POINT = (By.XPATH, "(//label[contains(@class,'PickUpDropSelection_pickDropItem')])[4]")
    CONTINUE_BTN = (By.XPATH, "//div[contains(@class, 'PickUpDropSelection_bottomSectionContainer')]//button[contains(@class, 'Button_primary')] | //button[contains(@class,'Button_primary') and text()='CONTINUE']")