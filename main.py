from datetime import datetime

from dotenv import load_dotenv

from src.execute_driver import execute_driver_instructions
from src.utilities.web_driver_utility import WDUtility
from src.utilities.execution_utility import ExecutionUtility
from src.share_data import send_data_to_team
from src.handle_launch_arguments import handle_launch_arguments


load_dotenv()


def main():
    today = datetime.now()
    day_of_the_week = today.strftime('%A')
    created_execution_executable_and_url = dict()

    driver_options, build_version = handle_launch_arguments()

    driver_utility = WDUtility(options=driver_options)

    executables = ['Release', 'Final'] if day_of_the_week in ('Monday', 'Thursday') else ['Release']
    for executable in executables:
        execution_utility = ExecutionUtility(build_version, driver_utility, executable, platform='PC')
        execute_driver_instructions(execution_utility, driver_utility)

        build_version = execution_utility.build_version

        confirm_execution_created_id = "bulk-defects-button-div"
        execution_url = driver_utility.get_current_url(confirm_execution_created_id)

        created_execution_executable_and_url[executable] = execution_url
    send_data_to_team(
        driver_utility, day_of_the_week, executables, build_version, created_execution_executable_and_url
    )


if __name__ == '__main__':
    main()
