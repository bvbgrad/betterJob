import app.utils6L.utils6L as utils

import argparse
import logging
import os
import PySimpleGUI as sg

from app.model.Company import Company

author = __author__ = 'Brent V. Bingham'
version = __version__ = '0.1'

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)


@utils.log_wrap
def menu():
    args = getargs()
    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))

    # ------ GUI Defintion ------ #

    menu_def = [
            ['File',
                ['Open', 'Save', 'Properties', 'Exit']],
            ['Features',
                ['Add Company', 'List companies']],
            ['Daily Tasks',
                ['Identify Job resources',
                    'Track events',
                    'Log face-to-face']],
            ['Help',
                ['Instructions', 'About...']],
            ]

    layout = [
                [sg.Menu(menu_def, )],
                [sg.Text('', size=(20, 8))],
                [sg.Text(
                    f"Options: {args}", relief=sg.RELIEF_SUNKEN,
                    size=(55, 1), pad=(0, 3), key='-status-')
                 ]
            ]

    window = sg.Window(
        '"Find a Better Job" Job Resource Manager',
        layout, default_element_size=(40, 1), grab_anywhere=False)

    # --- Menu Loop --- #
    while True:
        event, value = window.read()
        logger.info(f"Menu event='{event}'")
        if event == sg.WIN_CLOSED or event == 'Exit' or event is None:
            break       # exit event clicked
        elif event == 'Add Company':
            new_company()
        elif event == 'List companies':
            get_company_list()
        elif event == '-cpu-':
            pass        # add your call to launch a CPU measuring utility
    window.close()


@utils.log_wrap
def new_company():
    company = Company(name="Ancestory")
    company.add_company(company)


@utils.log_wrap
def get_company_list():
    company = Company(name='Ancestory')

    company_count = company.get_company_count()
    print(f"total number of companies = {company_count}")

    company_list = company.get_company_by_name(company.name)
    print(
        f"Company List for {company.name} = {company_list}")

    print(f"Company List = {company.get_all_companies()}")


@utils.log_wrap
def getargs():
    parser = argparse.ArgumentParser(
        description="Track and log job search activities")
    parser.add_argument(
        '-v', '--verbose', default=False, action="store_true",
        help='Provide detailed information')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {version}')
    args = parser.parse_args()
    return args
