"""
"""

import app.utils6L.utils6L as utils

import logging
import os
import PySimpleGUI as sg

from app.model.Company import Address

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)


@utils.log_wrap
def view_edit_company(company_name):
    logger.info(__name__ + ".view_edit_company()")
    event, values = sg.Window(
                    "Edit company name",
                    [[sg.T('Company name:', size=(12, 1)),
                        sg.In(
                            key='-COMPANY_NAME-',
                            size=(35, 1))],
                        [sg.OK()]]).read(close=True)
    new_company_name = values['-COMPANY_NAME-']
    return new_company_name


@utils.log_wrap
def view_create_link_address(address: Address) -> Address:
    logger.info(__name__ + ".view_create_link_address()")

    layout = [
        [sg.T('Street:', size=(8, 1)),
            sg.In(key='-STREET-', size=(50, 1))],
        [sg.T('City:', size=(8, 1)),
            sg.In(key='-CITY-', size=(30, 1))],
        [sg.T('State:', size=(8, 1)),
            sg.In(key='-STATE-', size=(2, 1))],
        [sg.T('Zip Code:', size=(8, 1)),
            sg.In(key='-ZIP_CODE-', size=(5, 1))],
        [sg.Submit()]
    ]

    event, values = sg.Window("Link address", layout=layout).read(close=True)

    address.street = values['-STREET-']
    address.city = values['-CITY-']
    address.state = values['-STATE-']
    address.zip_code = values['-ZIP_CODE-']

    return address
