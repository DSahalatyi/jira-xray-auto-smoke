from loguru import logger
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WDUtility:

    def __init__(self, options=None):
        self.driver = webdriver.Chrome(options=options)

    def waiter(self, element_id=None, element_xpath=None, is_clickable=False):
        selector = (By.ID, element_id) if element_id else (By.XPATH, element_xpath)
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(selector) if is_clickable else
                EC.presence_of_element_located(selector)
            )
        except TimeoutException:
            logger.error(f"Element '{selector}' cannot be found on web page")
            exit()

    def find_and_click_element(self, element_id=None, element_xpath=None):
        selector = (By.ID, element_id) if element_id else (By.XPATH, element_xpath)
        try:
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(selector))
        except TimeoutException:
            logger.error(f"Element '{element_id}' cannot be found on web page")
            exit()
        self.driver.find_element(*selector).click()

    def get_first_option_of_hidden_select(self, select_xpath):
        WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, select_xpath)))
        return self.driver.find_element(By.XPATH, f"{select_xpath}/option[1]")

    def enter_text_to_textarea(self, textarea_id=None, textarea_xpath=None, texts_to_enter=None):
        textarea_selector = (By.ID, textarea_id) if textarea_id else (By.XPATH, textarea_xpath)
        textarea = self.driver.find_element(*textarea_selector)
        textarea.clear()
        if isinstance(texts_to_enter, list):
            for text in texts_to_enter:
                textarea.send_keys(text)
                textarea.send_keys(Keys.RETURN)
        else:
            textarea.send_keys(texts_to_enter)

    def send_text_to_autocomplete_textarea(self, textarea_id, text_to_send=None, autocomplete_key=None):
        textarea = self.driver.find_element(By.ID, textarea_id)
        textarea.send_keys(text_to_send)
        textarea.send_keys(getattr(Keys, autocomplete_key))

    def remove_items_from_representation(self, representation_xpath, item_xpath, items_to_remove):
        representation = self.driver.find_element(By.XPATH, representation_xpath)
        items_in_representation = representation.text.split()
        for index in range(len(items_in_representation)):
            test_element = self.driver.find_element(By.XPATH, item_xpath.format(index))
            if test_element.text in items_to_remove:
                items_to_remove.remove(test_element.text)
                self.driver.execute_script("arguments[0].remove();", test_element)
        if len(items_to_remove) > 0:
            logger.error(f'Not removed items: {", ".join(items_to_remove)}')
            exit()

    def remove_items_from_hidden_select(self, item_xpath, items_to_remove):
        select_option_index = 1
        while True:
            try:
                select_option = self.driver.find_element(By.XPATH, item_xpath.format(select_option_index))
            except NoSuchElementException:
                break

            item = select_option.get_attribute('value')
            if item in items_to_remove:
                self.driver.execute_script("arguments[0].remove();", select_option)
                items_to_remove.remove(item)
                # To fix cycle jumping over index on removal
                select_option_index -= 1 if select_option_index != 1 else 1
            select_option_index += 1

        if len(items_to_remove) > 0:
            logger.error(f'Not removed items: {", ".join(items_to_remove)}')
            exit()

    def get_current_url(self, element_to_look_for=None):
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, element_to_look_for)))
        except TimeoutException:
            print("Loading took too much time!")
        return self.driver.current_url
