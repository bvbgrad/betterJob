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


@utils.log_wrap
def create_table(data, table_title=''):
    logger.info(__name__ + ".create_table()")

    if len(data) == 0:
        logger.warn(__name__ + ".create_table() No data provided for table")
        return None

    results = []
    headings = [str(data[0][x]) for x in range(len(data[0]))]

    layout = [[sg.Table(
        values=data[1:][:], headings=headings,
        max_col_width=25,
        # background_color='light blue',
        auto_size_columns=True,
        display_row_numbers=False,
        justification='left',
        # num_rows=20,
        alternating_row_color='lightyellow',
        key='-TABLE-',
        row_height=20,
        tooltip='This is a table')],
        [sg.Button('Select'), sg.Button('Exit')],
        [sg.Text('Select= read which rows are selected')]]

    window = sg.Window(table_title, layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Select':
            for row in values['-TABLE-']:
                results.append(data[row + 1])
        elif event == 'Update':
            window['-TABLE-'].update(values=data)

    window.close()
    return(results)
