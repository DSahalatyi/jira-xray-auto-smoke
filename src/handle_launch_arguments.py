import argparse
import os

from selenium.webdriver.chrome.options import Options


def handle_launch_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-hl', '--headless', required=False, action='store_true',
                        help='start browser in headless mode')
    parser.add_argument('-b', '--build', type=str, required=False, default=None, nargs='?',
                        help='specify build version if not latest')
    parser.add_argument('-sconf', '--skip_confirmation', required=False, action='store_true',
                        help='skip execution creation confirmation')
    args = parser.parse_args()

    options = Options()

    if args.headless:
        options.add_argument('window-size=1920,1080')
        options.add_argument('ignore-certificate-errors')
        options.add_argument('headless')
    options.add_argument('start-maximized')

    build_template = os.getenv('BUILD_TEMPLATE')
    if build_template not in args.build:
        raise EnvironmentError(f'Please use a correct build name form: {build_template}XXXX.0')
    build_version = args.build

    skip_confirmation = None
    if args.skip_confirmation:
        skip_confirmation = True

    return options, build_version, skip_confirmation
