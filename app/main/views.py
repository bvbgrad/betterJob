"""
"""

import app.utils6L.utils6L as utils

import logging
import os
import PySimpleGUI as sg

from app.model.Company import Address
# from app.model.Job_Action import Job

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
def create_table(header, data, table_title='', show_id=False):
    logger.info(__name__ + ".create_table()")

    if len(data) == 0:
        logger.warn(__name__ + ".create_table() No data provided for table")
        return None

    results = []
    if show_id:
        visible_column_map = None
    else:
        visible_column_map = \
            [False, True, False, True, True, True, True, True]

    layout = [
        [
            sg.CB('Address', enable_events=True, key='-ADDRESS-')
        ],
        [sg.Table(
            values=data[0:][:], headings=header,
            max_col_width=25,
            # background_color='light blue',
            auto_size_columns=True,
            visible_column_map=visible_column_map,
            display_row_numbers=False,
            justification='left',
            # num_rows=20,
            alternating_row_color='lightyellow',
            key='-TABLE-', enable_events=True,
            row_height=20,
            tooltip='This is a table')],
        [sg.Button('Exit')]
    ]

    window = sg.Window(table_title, layout)
    while True:
        event, values = window.read()
        print(event, values)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        elif event == '-TABLE-':
            if len(values['-TABLE-']) > 1:
                for row in values['-TABLE-']:
                    results.append(data[row])
            else:
                print(f"Action: {data[values['-TABLE-'][0]]}")
                results = data[values['-TABLE-'][0]]
        elif event == 'Update':
            window['-TABLE-'].update(values=data)

    window.close()
    return(results)
