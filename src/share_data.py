import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def send_data_to_team(driver_utility, day_of_the_week, executables, build_version, test_execution_executable_and_url):

    driver_utility.driver.get(os.getenv('MSTEAMS_DESTINATION_CHAT'))

    ms_teams_chat_frame_xpath = "//iframe[contains(@id, 'experience-container-')]"
    driver_utility.waiter(element_xpath=ms_teams_chat_frame_xpath)
    ms_teams_chat_frame = driver_utility.driver.find_element(By.XPATH, ms_teams_chat_frame_xpath)
    driver_utility.driver.switch_to.frame(ms_teams_chat_frame)

    message_textarea_xpath = "//div[contains(@id, 'new-message-')]"
    driver_utility.waiter(element_xpath=message_textarea_xpath, is_clickable=True)
    message_textarea = driver_utility.driver.find_element(By.XPATH, message_textarea_xpath)

    message_textarea.click()
    message_to_share_template = os.getenv('MESSAGE_TO_SHARE_TEMPLATE')
    message_to_share = message_to_share_template.format(
        day_of_the_week, ', '.join(executables), build_version
    ).split('\\n')

    for text in message_to_share:
        message_textarea.send_keys(text)
        message_textarea.send_keys(Keys.SHIFT, Keys.RETURN)
    for k, v in test_execution_executable_and_url.items():
        message_textarea.send_keys(f'{k}: {v}')
        message_textarea.send_keys(Keys.SHIFT, Keys.RETURN)
    message_textarea.send_keys(Keys.BACKSPACE)
    message_textarea.send_keys(Keys.RETURN)
    # Wait for message to get delivered before closing driver
    time.sleep(3)
