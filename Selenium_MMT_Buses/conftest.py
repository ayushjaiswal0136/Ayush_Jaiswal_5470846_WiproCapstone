import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


@pytest.fixture()
def driver():

    logger.info("========== STARTING TEST ==========")

    options = Options()

    # MAXIMIZE WINDOW
    options.add_argument("--start-maximized")

    # DISABLE POPUPS
    options.add_argument("--disable-notifications")

    options.add_argument("--disable-popup-blocking")

    # REMOVE SELENIUM DETECTION ISSUES
    options.add_experimental_option(
        "excludeSwitches",
        ["enable-automation"]
    )

    options.add_experimental_option(
        "useAutomationExtension",
        False
    )

    # CREATE DRIVER
    driver = webdriver.Chrome(
        service=Service(
            executable_path="drivers/chromedriver.exe"
        ),
        options=options
    )

    # IMPORTANT
    driver.maximize_window()

    # REMOVE WEBDRIVER FLAG
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    # WAITS
    driver.implicitly_wait(10)

    # OPEN WEBSITE
    logger.info("OPENING MAKEMYTRIP WEBSITE")

    driver.get(
        "https://www.makemytrip.com/bus-tickets/"
    )

    logger.info(
        f"CURRENT URL: {driver.current_url}"
    )

    yield driver

    logger.info("========== CLOSING TEST ==========")

    try:

        driver.quit()

        logger.info("BROWSER CLOSED SUCCESSFULLY")

    except Exception as e:

        logger.error(
            f"ERROR CLOSING BROWSER: {str(e)}"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call":

        if "driver" not in item.funcargs:
            return

        driver = item.funcargs["driver"]

        try:

            if report.passed:

                logger.info(
                    "TEST PASSED - CAPTURING SCREENSHOT"
                )

                path = ScreenshotUtil.capture(
                    driver,
                    f"{item.name}_PASS"
                )

            else:

                logger.error(
                    "TEST FAILED - CAPTURING SCREENSHOT"
                )

                path = ScreenshotUtil.capture(
                    driver,
                    f"{item.name}_FAIL"
                )

            allure.attach.file(
                path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

        except Exception as e:

            logger.error(
                f"SCREENSHOT FAILED: {str(e)}"
            )