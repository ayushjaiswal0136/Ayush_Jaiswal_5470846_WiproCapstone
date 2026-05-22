from selenium.webdriver.common.by import By


class BusSearchLocators:
    # ==========================================
    # FOR END TO END TEST
    # ==========================================
    BUS_RESULTS = (
        By.CSS_SELECTOR, "div[class*='BusCard_listingCard'], div[id^='listing-bus-card']"
    )
    AC_FILTER_BTN = (
        By.CSS_SELECTOR, "ul[class*='FilterTabs_tabCtr'] div[class*='FilterTabs_tabSection']"
    )
    FIRST_SELECT_SEATS_BTN = (
        By.CSS_SELECTOR, "div[id^='listing-bus-card'] button[class*='button'], div[id^='listing-bus-card'] button"
    )
    AVAILABLE_SEATS = (
        By.CSS_SELECTOR, "div[class*='Tooltip_tooltipWrapper'] img[alt='SEATER'], div[class*='Tooltip_tooltipWrapper'] img[alt='SLEEPER']"
    )
    # Improved locators for boarding and dropping points
    FIRST_BOARDING_POINT = (
        By.XPATH, "(//div[contains(@class, 'pickUp')]//label)[1] | (//label[contains(@class,'PickUpDropSelection_pickDropItem')])[1]"
    )
    FIRST_DROPPING_POINT = (
        By.XPATH, "(//div[contains(@class, 'drop')]//label)[1] | (//label[contains(@class,'PickUpDropSelection_pickDropItem')])[last()]"
    )
    # UPDATED: Catching dynamic "Continue" or "Book Seats" state-change buttons safely
    CONTINUE_BTN = (
        By.XPATH,"//div[contains(@class, 'cta-book-wrapper')]//button | //div[contains(@class, 'bottomSection')]//button | //button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'continue')] | //button[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'book seat')]"
    )
    ROUTE_TITLE = (By.CSS_SELECTOR, "h1[class*='seo-title']")
    SLEEPER_FILTER_BTN = (By.XPATH,
                          "//div[contains(@class, 'FilterTabs')]//span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sleeper')]")
    BUS_CARD_NAMES = (
        By.CSS_SELECTOR, "div[class*='makeFlex'] span[class*='latoBlack']"
    )
    SELECTED_SEAT_TEXT = (
        By.CSS_SELECTOR, "span[class*='seat-number']"
    )
    NO_BUSES_MSG = (
        By.CSS_SELECTOR, "div[class*='error-message'], span[class*='no-buses']"
    )

    # ==========================================
    # FOR INDIVIDUAL TESTS
    # ==========================================

    ROUTE_TITLE = (
        By.XPATH, "//h1[@data-testid='listing-title']"
    )
    SLEEPER_FILTER_BTN = (
        By.XPATH, "//p[text()='Sleeper']/parent::div | //span[text()='Sleeper']/ancestor::li"
    )
    ACTIVE_SLEEPER_FILTER = (
        By.XPATH, "//div[contains(@class,'activeTabs')]//p[text()='Sleeper']"
    )
    SELECTED_SEAT_TEXT = (
        By.XPATH, "//span[contains(.,'Seat No')]"
    )
    NO_BUSES_MSG = (
        By.XPATH, "//*[contains(text(),'No bus found on this route')]"
    )
    BOOKING_HEADING = (
        By.XPATH, "//h1[contains(text(),'Complete your booking')]"
    )