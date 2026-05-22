# import time
# import os
# import allure
# from seleniumbase import Driver
# from utils.logger import LogGen
# from utils.screenshot_util import ScreenshotUtil
# from utils.config_reader import ConfigReader
#
# logger = LogGen.loggen()
#
#
# def before_scenario(context, scenario):
#     logger.info(f"========== STARTING SCENARIO: {scenario.name} ==========")
#
#     # Using SeleniumBase UC Mode to bypass MakeMyTrip bot detection
#     context.driver = Driver(uc=True)
#     context.driver.maximize_window()
#
#     context.driver.implicitly_wait(ConfigReader.get_implicit_wait())
#
#     # Launching directly to the bus tickets page as per your old logic
#     base_url = "https://www.makemytrip.com/bus-tickets/"
#     logger.info(f"OPENING MAKEMYTRIP WEBSITE: {base_url}")
#     context.driver.get(base_url)
#
#     # CRITICAL WAF WAIT: Let invisible security scripts resolve
#     time.sleep(2)
#     logger.info(f"CURRENT URL: {context.driver.current_url}")
#
#
# def after_step(context, step):
#     # This acts like your pytest_runtest_makereport hook
#     try:
#         if step.status == "failed":
#             logger.error(f"STEP FAILED: {step.name} - CAPTURING SCREENSHOT")
#             path = ScreenshotUtil.capture_screenshot(context.driver, f"FAIL_{step.name[:20]}")
#
#             with open(path, "rb") as image_file:
#                 allure.attach(
#                     image_file.read(),
#                     name=f"Failed: {step.name}",
#                     attachment_type=allure.attachment_type.PNG
#                 )
#
#         elif step.status == "passed":
#             logger.info(f"STEP PASSED: {step.name} - CAPTURING SCREENSHOT")
#             path = ScreenshotUtil.capture_screenshot(context.driver, f"PASS_{step.name[:20]}")
#
#             with open(path, "rb") as image_file:
#                 allure.attach(
#                     image_file.read(),
#                     name=f"Passed: {step.name}",
#                     attachment_type=allure.attachment_type.PNG
#                 )
#     except Exception as e:
#         logger.error(f"SCREENSHOT FAILED: {str(e)}")
#
#
# def after_scenario(context, scenario):
#     logger.info(f"========== CLOSING SCENARIO: {scenario.name} ==========")
#     if hasattr(context, 'driver'):
#         try:
#             context.driver.quit()
#             logger.info("BROWSER CLOSED SUCCESSFULLY")
#         except Exception as e:
#             logger.error(f"ERROR CLOSING BROWSER: {str(e)}")
#
# def after_all(context):
#
#     print(
#         "\n======= TESTS COMPLETED - OPENING ALLURE REPORT ======="
#     )
#
#     os.system(
#         "allure serve reports/allure-results"
#     )

import time
import os
import allure

from seleniumbase import Driver

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader

logger = LogGen.loggen()


def before_scenario(context, scenario):

    logger.info(
        f"========== STARTING SCENARIO: {scenario.name} =========="
    )

    # USING SELENIUMBASE UC MODE
    context.driver = Driver(
        uc=True
    )

    context.driver.maximize_window()

    context.driver.implicitly_wait(
        ConfigReader.get_implicit_wait()
    )

    # OPEN WEBSITE
    base_url = "https://www.makemytrip.com/bus-tickets/"

    logger.info(
        f"OPENING MAKEMYTRIP WEBSITE: {base_url}"
    )

    context.driver.get(
        base_url
    )

    # WAF WAIT
    time.sleep(2)

    logger.info(
        f"CURRENT URL: {context.driver.current_url}"
    )


def after_step(context, step):

    try:

        if step.status == "failed":

            logger.error(
                f"STEP FAILED: {step.name} - CAPTURING SCREENSHOT"
            )

            path = ScreenshotUtil.capture_screenshot(
                context.driver,
                f"FAIL_{step.name[:20]}"
            )

            allure.attach.file(
                path,
                name=step.name,
                attachment_type=allure.attachment_type.PNG
            )

        elif step.status == "passed":

            logger.info(
                f"STEP PASSED: {step.name} - CAPTURING SCREENSHOT"
            )

            path = ScreenshotUtil.capture_screenshot(
                context.driver,
                f"PASS_{step.name[:20]}"
            )

            allure.attach.file(
                path,
                name=step.name,
                attachment_type=allure.attachment_type.PNG
            )

    except Exception as e:

        logger.error(
            f"SCREENSHOT FAILED: {str(e)}"
        )


def after_scenario(context, scenario):

    logger.info(
        f"========== CLOSING SCENARIO: {scenario.name} =========="
    )

    if hasattr(context, 'driver'):

        try:

            with open("logs/automation.log", "r") as log_file:

                allure.attach(
                    log_file.read(),
                    name="Execution Logs",
                    attachment_type=allure.attachment_type.TEXT
                )

            context.driver.quit()

            logger.info(
                "BROWSER CLOSED SUCCESSFULLY"
            )

        except Exception as e:

            logger.error(
                f"ERROR CLOSING BROWSER: {str(e)}"
            )


def after_all(context):

    print(
        "\n======= TESTS COMPLETED - OPENING ALLURE REPORT ======="
    )

    os.system(
        "allure generate reports/allure-results -o reports/allure-report --clean"
    )

    os.system(
        "allure open reports/allure-report"
    )