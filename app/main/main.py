import logging
import os

import app.utils6L.utils6L as utils
from app.main.config import getargs, get_config, save_config, get_version
import PySimpleGUI as sg

from app.main.address_ctlr import link_address_to_company, get_address_list
from app.main.address_ctlr import delete_address
from app.main.company_ctlr import get_company_address_table_data
from app.main.company_ctlr import company_details
from app.main.company_ctlr import add_new_company, edit_company, delete_company
from app.main.job_ctlr import add_job, get_job_data

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)

NO_COMPANY_ADDRESS = 'No company address'


@utils.log_wrap
def menu():
    logger.info(__name__ + ".menu()")
    logger.info(f"{get_version()}\nUsing {sg}\nVersion{sg.version}")
    args = getargs()
    config = get_config()

    sg.ChangeLookAndFeel(config["theme"]["lookandfeel"])
    # sg.SetOptions(element_padding=(0, 0), font=config["theme"]["font"], auto_size_text=True)
    sg.SetOptions(element_padding=(0, 0), font=12, auto_size_text=True)

    # ------ GUI Defintion ------ #

    company_submenu = [
        'Add new company',
        'Delete company',
        'Edit company']
    address_submenu = [
        'Add address',
        'Delete address',
        'Edit address',
        'Link address',
        'List addresses']
    job_submenu = [
        'Add New Job',
        'List jobs']

    menu_def = [
        ['File',
            ['Open', 'Save', 'Properties', 'Exit']],
        ['Edit',
            ['Company', company_submenu,
                'Address', address_submenu,
                'Job', job_submenu]],
        ['Daily Tasks',
            ['Identify Job resources',
                'Track events',
                'Log face-to-face']],
        ['Help',
            ['Instructions', 'About...']],
    ]

    if args.index:
        company_address_visible_column_map = None
        job_action_visible_column_map = None
    else:
        company_address_visible_column_map = \
            [False, True, False, True, True, True, True, True]
        job_action_visible_column_map = \
            [False, True, True, True, True, True, True, True, True, True]

    company_address_header = \
        ['Id', 'Name', 'Id', 'Street', 'City', 'State', 'Zip', 'Jobs']

    company_address_data = get_company_address_table_data()
    company_address_rows = len(company_address_data)
    company_locations_text = \
        f"There are {company_address_rows} company locations."
    company_tab_layout = [
        [sg.CB(
            'Address', default=True,
            enable_events=True, key='-CB_ADDRESS-')],
        [sg.Text(
            company_locations_text,
            key='-NBR_COMPANIES-')],
        [sg.Table(
            values=company_address_data,
            headings=company_address_header,
            right_click_menu=['', company_submenu],
            max_col_width=25,
            auto_size_columns=True,
            visible_column_map=company_address_visible_column_map,
            display_row_numbers=False,
            justification='left',
            alternating_row_color='lightyellow',
            row_height=20,
            key='-COMPANY_TABLE-', enable_events=True,
            tooltip='This table shows company and address information')]
    ]

    job_table_header = \
        ['Id  ', 'Name', 'Number', 'Status', 'Type',
            'Posted', 'Expire', 'Min $', 'Max $', 'Company']

    job_data = get_job_data()
    if len(job_data) == 0:
        job_action_tab_layout = \
            [[sg.Text('Please use Edit menu to add a job.')]]
    else:
        job_action_tab_layout = [
            [sg.Text(f"There are {len(job_data)} jobs", key='-NBR_JOBS')],
            [sg.Table(
                values=job_data,
                headings=job_table_header,
                right_click_menu=['', job_submenu],
                max_col_width=25,
                auto_size_columns=True,
                visible_column_map=job_action_visible_column_map,
                display_row_numbers=False,
                justification='left',
                alternating_row_color='lightyellow',
                key='-JOB_TABLE-', enable_events=True,
                row_height=20,
                tooltip='This table shows job information')]
        ]

    networking_tab_layout = [[sg.Text('This is inside the networking tab')]]

    metrics_tab_layout = [[sg.Text('This is inside the metrics tab')]]

    layout = [[
        [sg.Menu(menu_def, key='-MENU-')],
        [sg.Text(
            f"Options: {args}", relief=sg.RELIEF_SUNKEN,
            size=(55, 1), pad=(0, 3), key='-STATUS-')],
        sg.TabGroup([[
            sg.Tab('Networking', networking_tab_layout),
            sg.Tab('Companies', company_tab_layout),
            sg.Tab('Job Actions', job_action_tab_layout),
            sg.Tab('Metrics', metrics_tab_layout)
            ]], key='-TAB-')
    ]]

    window = sg.Window(
        '"Find a Better Job" Job Resource Manager (JRM)',
        layout, default_element_size=(40, 1),
        resizable=True, finalize=True)

    # --- Menu Loop --- #
    while True:
        refresh_all_table_info(window)
        event, values = window.read()
        logger.info(f"Menu event, values = '{event}', {values}")
        if event == sg.WIN_CLOSED or event == 'Exit' or event is None:
            break
        elif event == '-COMPANY_TABLE-':
            company_details(window, values['-COMPANY_TABLE-'], company_address_data)
        elif event == 'Add new company':
            add_new_company()
        elif event == 'Edit company':
            edit_company(values['-COMPANY_TABLE-'])
        elif event == 'Delete company':
            delete_company()
        elif event == 'Link address':
            link_address_to_company(values['-COMPANY_TABLE-'])
        elif event == 'List addresses':
            get_address_list()
        elif event == 'Delete address':
            delete_address(window, values['-LB_Address-'])
        elif event == 'Add New Job':
            add_job()
        elif event == 'About...':
            about_text = f"{get_version()}\n\nUsing {sg}\nVersion{sg.version}"
            sg.popup(about_text, title="About JRM")

    # All done - exiting
    save_config(config)
    window.close()


@utils.log_wrap
def refresh_all_table_info(window):
    logger.info(__name__ + ".refresh_all_table_info()")

    company_address_data = get_company_address_table_data()
    company_address_rows = len(company_address_data)
    company_locations_text = \
        f"There are {company_address_rows} company locations."
    window['-NBR_COMPANIES-'].update(company_locations_text)
    window['-COMPANY_TABLE-'].update(company_address_data)
