import argparse
import logging
import os

import app.utils6L.utils6L as utils
import PySimpleGUI as sg

from app.main.address_ctlr import link_address_to_company, get_address_list
from app.main.address_ctlr import delete_address
from app.main.company_ctlr import get_company_address_table_data
from app.main.company_ctlr import get_company_list, create_company_table
from app.main.company_ctlr import work_company_details, get_selected_company
from app.main.company_ctlr import add_new_company, edit_company, delete_company
from app.main.job_ctlr import add_job, get_job_data
from app.model import db_session
from app.model.Company import Address, Company

author = __author__ = 'Brent V. Bingham'
version = __version__ = '0.1'

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)

NO_COMPANY_ADDRESS = 'No company address'


@utils.log_wrap
def menu():
    logger.info(__name__ + ".menu()")
    args = getargs()
    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))

    # ------ GUI Defintion ------ #

    company_submenu = [
        'Add new company',
        'Delete company',
        'Edit company',
        'List companies',
        'Show companies']
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

    company0_layout = [
        [sg.Listbox(
            values=['Click here to display company info'], enable_events=True,
            right_click_menu=['', company_submenu],
            key='-LB_Company-', size=(30, 10))],
        [sg.Listbox(
            values=[NO_COMPANY_ADDRESS], enable_events=True,
            right_click_menu=['', address_submenu],
            key='-LB_Address-', size=(30, 2))]
        ]

    companies_col1_layout = [[sg.Frame('Companies', layout=company0_layout)]]
    companies_col2_layout = [[sg.Text('Company Jobs')]]

    company0_tab_layout = [
                [sg.Column(companies_col1_layout),
                    sg.Column(companies_col2_layout)]
            ]

    company_address_header = \
        ['Id', 'Name', 'Id', 'Street', 'City', 'State', 'Zip', 'Jobs']

    company_address_data = get_company_address_table_data()
    company_address_rows = len(company_address_data)
    company_locations_text = \
        f"There are {company_address_rows} company locations."
    company1_tab_layout = [
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
            key='-COMPANY_TABLE-', enable_events=True,
            row_height=20,
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
        [sg.Menu(menu_def, )],
        [sg.Text(
            f"Options: {args}", relief=sg.RELIEF_SUNKEN,
            size=(55, 1), pad=(0, 3), key='-status0-')],
        sg.TabGroup([[
            sg.Tab('Networking', networking_tab_layout),
            sg.Tab('Companies (List Box)', company0_tab_layout),
            sg.Tab('Companies (Table)', company1_tab_layout),
            sg.Tab('Job Actions', job_action_tab_layout),
            sg.Tab('Metrics', metrics_tab_layout)
            ]])
    ]]

    window = sg.Window(
        '"Find a Better Job" Job Resource Manager (JRM)',
        layout, default_element_size=(40, 1),
        resizable=True, finalize=True)

    # --- Menu Loop --- #
    while True:
        refresh_all_table_info(window)
        event, values = window.read()
        logger.info(f"Menu event='{event}'")
        if event == sg.WIN_CLOSED or event == 'Exit' or event is None:
            break
        elif event == '-LB_Company-':
            work_company_details(window, values['-LB_Company-'])
        elif event == 'Display Company list':
            refresh_company_info(window)
        elif event == 'Add new company':
            add_new_company()
            refresh_company_info(window)
        elif event == 'Edit company':
            edit_company(values['-LB_Company-'])
            refresh_company_info(window)
        elif event == 'List companies':
            get_company_list()
        elif event == 'Show companies':
            show_company_table()
        elif event == 'Delete company':
            delete_company()
        elif event == 'Link address':
            link_address_to_company(values['-LB_Company-'])
            refresh_company_info(window)
        elif event == 'List addresses':
            get_address_list()
        elif event == 'Delete address':
            delete_address(window, values['-LB_Address-'])
            company01 = get_selected_company(values['-LB_Company-'])
            refresh_address_info(window, company01)
        elif event == 'Add New Job':
            add_job()
    window.close()


@utils.log_wrap
def refresh_all_table_info(window):
    logger.info(__name__ + ".refresh_all_table_info()")

    refresh_company_info(window)

    company_address_data = get_company_address_table_data()
    company_address_rows = len(company_address_data)
    company_locations_text = \
        f"There are {company_address_rows} company locations."
    window['-NBR_COMPANIES-'].update(company_locations_text)
    window['-COMPANY_TABLE-'].update(company_address_data)


@utils.log_wrap
def refresh_address_info(window, company):
    logger.info(__name__ + ".refresh_address_info()")

    address01 = Address()
    if company is None:
        sg.popup("Please select a company")
    else:
        with db_session() as db:
            address_list = \
                address01.get_address_by_company(db, company.company_Id)
            addresses = []
            for loc in address_list:
                address = \
                    f"{loc.street}*{loc.city}*{loc.state}*{loc.zip_code}"
                addresses.append(address)

        if len(addresses) > 0:
            window['-LB_Address-'].update(sorted(addresses))
        else:
            window['-LB_Address-'].update([NO_COMPANY_ADDRESS])


@utils.log_wrap
def refresh_company_info(window):
    logger.info(__name__ + ".refresh_company_info()")
    company01 = Company()
    with db_session() as db:
        company_list = company01.get_all_companies(db)
        company_names = []
        for company in company_list:
            company_names.append(company.name)
        window['-LB_Company-'].update(sorted(company_names))
        refresh_address_info(window, company01)


@utils.log_wrap
def show_company_table():
    logger.info(__name__ + ".show_company_table()")

    header = ['Id', 'Name', 'Id', 'Street', 'City', 'State', 'Zip', 'Jobs']

    data = get_company_address_table_data()
    # result = create_table(header, data, show_id=True)
    result = create_company_table(header, data)
    if result is None:
        logger.info(__name__ + ".show_company_table() Error result")
    print(f'Show table result: {result}')


@utils.log_wrap
def getargs():
    logger.info(__name__ + ".getargs()")
    parser = argparse.ArgumentParser(
        description="Track and log job search activities")
    parser.add_argument(
        '-i', '--index', default=False, action="store_true",
        help='Display object indexes in tables')
    parser.add_argument(
        '-v', '--verbose', default=False, action="store_true",
        help='Provide detailed information')
    parser.add_argument(
        '--version', action='version', version='%(prog)s {version}')
    args = parser.parse_args()
    return args
