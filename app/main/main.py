import app.utils6L.utils6L as utils

import argparse
import logging
import os
import PySimpleGUI as sg

from app.model import db_session
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
                ['Add Company',
                    'Delete Company',
                    'List companies']],
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
        elif event == 'Delete Company':
            delete_company()
        elif event == 'List companies':
            get_company_list()
        elif event == '-cpu-':
            pass        # add your call to launch a CPU measuring utility
    window.close()


@utils.log_wrap
def new_company():
    logger.info(__name__ + ".new_company()")
    text = sg.popup_get_text('Get company name', 'Company name')
    if text is not None:
        if len(text) > 2:
            company = Company(name=text)
            with db_session() as db:
                try:
                    company.add_company(db, company)
                except ValueError as e:
                    sg.popup_no_titlebar(e)
        else:
            sg.popup("Company names must have at least 3 characters")


@utils.log_wrap
def delete_company():
    logger.info(__name__ + ".delete_company()")
    text = sg.popup_get_text(
        'Company name (Default: get list of all companies)',
        'Get company name')
    company = Company(name=text)

    with db_session() as db:
        # create blank company to use company instance methods
        company_count = company.get_company_count(db)
        if text == "" or text is None:
            company_list = company.get_all_companies(db)
        else:
            company_list = company.get_company_by_name(db, company.name)
        # confirm delete action
        number_to_delete = len(company_list)
        msg = f"Delete {number_to_delete} of {company_count} companies?"
        response = sg.popup_yes_no("Warning - Irreversible delete action", msg)
        if response == "Yes":
            response = sg.popup_ok_cancel(
                f"Delete these {number_to_delete} companies?\n{company_list}",
                title=f"Deleting {number_to_delete} companies",)
            if response == "OK":
                for company in company_list:
                    company.delete_company(db, company)
                sg.popup_no_titlebar(f"Deleted {number_to_delete} companies")


@utils.log_wrap
def get_company_list():
    logger.info(__name__ + ".get_company_list()")
    text = sg.popup_get_text(
        'Company name (Default: get list of all companies)',
        'Get company name')
    company = Company(name=text)
    with db_session() as db:
        if text == "" or text is None:
            company_list = company.get_all_companies(db)
        else:
            company_list = company.get_company_by_name(db, company.name)
        print(f"There are {len(company_list)} database entries for '{text}'")
        print(company_list)
    return company_list


@utils.log_wrap
def getargs():
    logger.info(__name__ + ".getargs()")
    parser = argparse.ArgumentParser(
        description="Track and log job search activities")
    parser.add_argument(
        '-v', '--verbose', default=False, action="store_true",
        help='Provide detailed information')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {version}')
    args = parser.parse_args()
    return args
