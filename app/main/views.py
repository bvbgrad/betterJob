"""
"""

import app.utils6L.utils6L as utils

import logging
import os
import PySimpleGUI as sg

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)


@utils.log_wrap
def edit_company(company):
    logger.info(__name__ + ".edit_company()")
    event, values = sg.Window(
                    "Edit company name",
                    [[sg.T('Company name:', size=(12, 1)),
                        sg.In(key='-COMPANY_NAME-', size=(35, 1))],
                        [sg.Button('Ok')]]).read(close=True)
    company.name = values['-COMPANY_NAME-']
    return company
