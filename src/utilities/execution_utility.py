import os
from datetime import datetime


class ExecutionUtility:

    def __init__(self, _build_version, driver_utility, executable, platform):
        self._build_version = _build_version
        self.driver_utility = driver_utility
        self.executable = executable
        self.platform = platform
        self.current_date = datetime.now().strftime("%d/%m/%Y")

    def open_create_execution_window(self):
        create_test_execution_button_id = "raven-add-testexecs"
        self.driver_utility.find_and_click_element(create_test_execution_button_id)

        all_tests_button_id = "raven-plan-create-te-link"
        self.driver_utility.find_and_click_element(all_tests_button_id)

    def fill_in_general_page(self):
        assign_to_me_id = "assign-to-me-trigger"
        self.driver_utility.find_and_click_element(assign_to_me_id)

        affected_version_id = "versions-textarea"
        self.driver_utility.send_text_to_autocomplete_textarea(
            affected_version_id, self.build_version, autocomplete_key='RETURN'
        )
        self.fill_in_summary()
        self.fill_in_description()

    def process_details_page(self):
        self.fill_in_test_environments()
        self.remove_executable_tests_from_representation()
        self.remove_executable_tests_from_hidden_select()

    @property
    def build_version(self):
        if self._build_version is None:
            build_version_select_id = '//*[@id="versions"]/optgroup[1]'
            self._build_version = self.driver_utility.get_first_option_of_hidden_select(
                build_version_select_id
            ).get_attribute("innerHTML").replace(' ', '').replace('\n', '')
        return self._build_version

    def fill_in_summary(self):
        summary_id = "summary"
        summary_template = os.getenv('SUMMARY_TEMPLATE')
        summary_to_paste = summary_template.format(self.executable, self.current_date, self.platform)
        self.driver_utility.enter_text_to_textarea(textarea_id=summary_id, texts_to_enter=summary_to_paste)

    def fill_in_description(self):
        frame_id = "mce_0_ifr"
        self.driver_utility.waiter(frame_id, 'is present')
        self.driver_utility.driver.switch_to.frame(frame_id)

        description_xpath = "/html/body/p"
        description_template = os.getenv('DESC_TEMPLATE')
        descriptions_to_paste = description_template.format(
            self.executable, self.current_date, self.platform, self.build_version
        ).split('\\n')
        self.driver_utility.enter_text_to_textarea(
            textarea_xpath=description_xpath, texts_to_enter=descriptions_to_paste
        )
        self.driver_utility.driver.switch_to.default_content()

    def fill_in_test_environments(self):
        text_to_send = [self.platform, self.executable]
        test_env_textarea_id = "customfield_12494-textarea"
        for text in text_to_send:
            self.driver_utility.send_text_to_autocomplete_textarea(
                textarea_id=test_env_textarea_id, text_to_send=text, autocomplete_key='SPACE'
            )

    def remove_executable_tests_from_representation(self):
        representation_xpath = '//*[@id="customfield_12484-multi-select"]/div[2]/ul'
        test_xpath = '//*[@id="item-row-{}"]'
        tests_to_remove = os.getenv('RELEASE_DEL_TESTS').split(',') if self.executable == 'Release' else \
            os.getenv('FINAL_DEL_TESTS').split(',')
        self.driver_utility.remove_items_from_representation(representation_xpath, test_xpath, tests_to_remove)

    def remove_executable_tests_from_hidden_select(self):
        test_xpath = '//*[@id="customfield_12484"]/option[{}]'
        tests_to_remove = os.getenv('RELEASE_DEL_TESTS').split(',') if self.executable == 'Release' else \
            os.getenv('FINAL_DEL_TESTS').split(',')
        self.driver_utility.remove_items_from_hidden_select(test_xpath, tests_to_remove)

    def press_create_button(self):
        create_button_id = "create-issue-submit"
        self.driver_utility.find_and_click_element(create_button_id)
