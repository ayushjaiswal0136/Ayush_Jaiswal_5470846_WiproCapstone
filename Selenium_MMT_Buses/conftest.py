import pytest
import allure
import time
import os

# IMPORT SELENIUMBASE
from seleniumbase import Driver

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


@pytest.fixture()
def driver():
    logger.info("========== STARTING TEST ==========")

    # CREATE DRIVER USING SELENIUMBASE UC MODE
    driver = Driver(uc=True)
    driver.maximize_window()

    # WAITS
    driver.implicitly_wait(5)

    # OPEN WEBSITE
    logger.info("OPENING MAKEMYTRIP WEBSITE")

    driver.get(
        "https://www.makemytrip.com/bus-tickets/"
    )

    # CRITICAL WAF WAIT: Let invisible security scripts resolve
    time.sleep(2)

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

# AUTO OPEN ALLURE REPORT
def pytest_unconfigure(config):

    print(
        "\n======= TESTS COMPLETED - OPENING ALLURE REPORT ======="
    )

    os.system(
        "allure generate reports/allure-results -o reports/allure-report --clean"
    )

    os.system(
        "allure open reports/allure-report"
    )