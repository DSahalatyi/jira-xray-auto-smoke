import os
import time


def execute_driver_instructions(execution_utility, driver_utility):
    # Wait for web page redirection between executions
    time.sleep(5)
    driver_utility.driver.get(os.getenv('TEST_PLAN_URL'))
    execution_utility.open_create_execution_window()
    execution_utility.fill_in_general_page()

    details_tab_element_id = "aui-uid-4"
    execution_utility.driver_utility.find_and_click_element(details_tab_element_id)

    execution_utility.process_details_page()

    while True:
        confirmation = input('Please confirm creation of a new test execution (y/n):\n')
        if confirmation == 'y':
            create_button_id = "create-issue-submit"
            driver_utility.find_and_click_element(create_button_id)
            break
        elif confirmation == 'n':
            print('Creation denied. Exiting...')
            exit()
        print('Please use y or n!')
