from PySimpleGUI.PySimpleGUI import popup_scrolled
import app.utils6L.utils6L as utils

import argparse
import logging
import os
import PySimpleGUI as sg

from app.model import db_session
from app.model.Company import Address, Company
from app.model.Job_Action import Job

from app.main.views import view_create_link_address, view_edit_company, \
        create_company_table

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

    if args.index:
        company_address_visible_column_map = None
    else:
        company_address_visible_column_map = \
            [False, True, False, True, True, True, True, True]

    company_address_header = \
        ['Id', 'Name', 'Id', 'Street', 'City', 'State', 'Zip', 'Jobs']

    company1_tab_layout = [
        [sg.CB('Address', default=True, enable_events=True, key='-ADDRESS-')],
        [sg.Table(
            values=get_company_address_table_data(),
            headings=company_address_header,
            max_col_width=25,
            auto_size_columns=True,
            visible_column_map=company_address_visible_column_map,
            display_row_numbers=False,
            justification='left',
            alternating_row_color='lightyellow',
            key='-TABLE-', enable_events=True,
            row_height=20,
            tooltip='This table shows company and address information')]
    ]

    job_action_tab_layout = [[sg.Text('This is inside the job action tab')]]

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
        '"Find a Better Job" Job Resource Manager',
        layout, default_element_size=(40, 1), resizable=True)

    # --- Menu Loop --- #
    first_loop = True
    while True:
        event, values = window.read()
        logger.info(f"Menu event='{event}'")
        if event == sg.WIN_CLOSED or event == 'Exit' or event is None:
            break
        elif first_loop:
            refresh_company_info(window, values['-LB_Company-'])
            first_loop = False
        elif event == '-LB_Company-':
            work_company_details(window, values['-LB_Company-'])
        elif event == 'Display Company list':
            refresh_company_info(window, values['-LB_Company-'])
        elif event == 'Add new company':
            add_new_company()
            refresh_company_info(window, values['-LB_Company-'])
        elif event == 'Edit company':
            edit_company(values['-LB_Company-'])
            refresh_company_info(window, values['-LB_Company-'])
        elif event == 'List companies':
            get_company_list()
        elif event == 'Show companies':
            show_company_table()
        elif event == 'Delete company':
            delete_company()
        elif event == 'Link address':
            link_address_to_company(values['-LB_Company-'])
            refresh_company_info(window, values['-LB_Company-'])
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
def add_new_address():
    logger.info(__name__ + ".add_new_address()")
    text = sg.popup_get_text('Get address', 'Street address')
    if text is not None:
        if len(text) > 2:
            address = Address(street=text)
            with db_session() as db:
                address.add_address(db, address)
        else:
            sg.popup("Addressess must have at least 3 characters")


def get_address_list():
    logger.info(__name__ + ".get_address_list()")
    address = Address()
    with db_session() as db:
        address_string = ""
        address_list = address.get_address_list(db)
        number_addresses = len(address_list)
        for address in address_list:
            address_string += f"\t{address}\n"
        popup_scrolled(
            f"There are {number_addresses} addresses:",
            f"{address_string}",
            title="Addresses in the database",
            size=(100, number_addresses))


@utils.log_wrap
def work_company_details(window, company_name):
    logger.info(__name__ + ".work_company_details()")

    if len(company_name) != 1:
        sg.popup("Please select a company")
    else:
        company01 = get_selected_company(company_name)
        msg = f"Display job postings for '{company01}'"
        sg.popup(msg)
        refresh_address_info(window, company01)


def get_selected_company(company_info):
    logger.info(__name__ + ".get_selected_company()")

    # can't get a company instance without a company name
    if len(company_info) == 0:
        return

    # just need an empty company instance for the query
    company01 = Company()
    company_name = company_info[0]
    with db_session() as db:
        company01 = company01.get_company_by_name(db, company_name)
    return company01


@utils.log_wrap
def add_new_company():
    logger.info(__name__ + ".new_company()")
    text = sg.popup_get_text('Enter company name', 'Company name')
    if text is not None:
        if len(text) > 1:
            company = Company(name=text)
            with db_session() as db:
                try:
                    company.add_company(db, company)
                except ValueError as e:
                    sg.popup_no_titlebar(e)
        else:
            sg.popup("Company names must have at least 2 characters")


@utils.log_wrap
def edit_company(company_info):
    logger.info(__name__ + ".edit_company()")
    # a blank company_info list means there is no company name to edit
    if len(company_info) == 0:
        sg.popup("Please select a company to edit")
    else:
        company_name = company_info[0]
        new_company_name = view_edit_company(company_name)
        # a blank return value means no no name change
        if new_company_name is not None and len(new_company_name) > 0:
            # company instance required to access Company methods
            company01 = Company()
            with db_session() as db:
                # replace company01 instance with prior company values
                company01 = company01.get_company_by_name(db, company_name)
                if company01:
                    company01.name = new_company_name
                    db.add(company01)
                else:
                    sg.popup("")


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
            print(f"Found a total of {len(company_list)} companies")
        else:
            company_list = company.get_company_by_name(db, company.name)
        print(f"Found {len(company_list)} database entities for '{text}'")
        print(company_list)
    return company_list


@utils.log_wrap
def link_address_to_company(company_info):
    logger.info(__name__ + ".link_address_to_company()")

    if len(company_info) == 1:
        company_name = company_info[0]
        msg = f"Link a new address to '{company_name}'?"
        response = sg.popup_yes_no(msg)
        if response == "Yes":
            address01 = Address()
            address01 = view_create_link_address(address01)
            if address01 is not None:
                company01 = Company()
                with db_session() as db:
                    company01 = company01.get_company_by_name(db, company_name)
                    address01.company_IdFK = company01.company_Id
                    address01.add_address(db, address01)
    else:
        sg.popup("Choose a company")


@utils.log_wrap
def delete_address(window, address):
    logger.info(__name__ + f".delete_address({address})")

    if len(address) != 1:
        sg.popup("Please select a single address to delete")
        return

    # address[0] is the candidate address to delete
    # unless it is the default value that indicates there are no addresses
    if address[0] == NO_COMPANY_ADDRESS:
        sg.popup("There is no address to delete")
        return

    # we have a single address to delete
    # create a skeleton address and scan the address list to find its equal
    ap = address[0].split('*')
    address01 = Address(ap[0], ap[1], ap[2], ap[3])
    with db_session() as db:
        addresses = address01.get_address_list(db)
        for address in addresses:
            address_found = False
            if address01 == address:
                address_found = True
                break
        if address_found:
            address.delete_self(db)
            logger.info(f"Deleted: {address}")
        else:
            logger.info(f"Not found: {address}")


@utils.log_wrap
def refresh_company_info(window, company_name):
    logger.info(__name__ + ".refresh_company_info()")
    company01 = Company()
    with db_session() as db:
        company_list = company01.get_all_companies(db)
        company_names = []
        for company in company_list:
            company_names.append(company.name)
        window['-LB_Company-'].update(sorted(company_names))


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
def add_job():
    logger.info(__name__ + ".add_job()")
    job01 = Job('test parameters', salary_min=110000, priority=5)
    with db_session() as db:
        job01.add_job(db, job01)

    with db_session() as db:
        print(f"There are {job01.get_job_count(db)} jobs")
        for i, job in enumerate(job01.get_all_jobs(db), 1):
            print(f"{i:2} --- {job}")

    print(f"new job just added: {job01}")


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
def get_company_address_table_data():
    logger.info(__name__ + ".show_company_table()")

    data = []
    company = Company()
    address = Address()
    job = Job()
    with db_session() as db:
        company_list = company.get_all_companies(db)
        for company in company_list:
            address_list = \
                address.get_address_by_company(db, company.company_Id)
            job_count = job.get_job_count_by_company(db, company.company_Id)
            for adr in address_list:
                data.append([
                        company.company_Id, company.name,
                        adr.address_Id, adr.street, adr.city,
                        adr.state, adr.zip_code,
                        job_count])
    return data


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
