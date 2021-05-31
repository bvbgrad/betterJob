"""
"""

import app.utils6L.utils6L as utils

import logging
import os
import PySimpleGUI as sg

from app.model import db_session
from app.model.Company import Company, Address
from app.model.Job_Action import Job
from app.main.views import view_edit_company
from app.main.views import create_company_table

# from app.model.Job_Action import Job

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)


@utils.log_wrap
def company_details(window, company_rows, company_address_data):
    logger.info(__name__ + ".company_details()")

    if len(company_rows) == 0:
        sg.popup("Please select a company", no_titlebar=True)
    else:
        company_data = company_address_data[company_rows[0]]
        msg = ''
        if company_data[7] > 0:
            job = Job()
            with db_session() as db:
                job_list = job.get_job_by_company(db, company_data[0])
                msg = f"{company_data[1]} has {company_data[7]} job postings"
                msg += f"{job_list}"
        else:
            msg = f"No job postings identified yet for '{company_data[1]}'"
        sg.popup(msg, no_titlebar=True)


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


# bvb TODO check references, may not need this module
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
    logger.info(__name__ + ".get_company_address_table_data()")

    data = []
    company = Company()
    address = Address()
    job01 = Job()
    with db_session() as db:
        company_list = company.get_all_companies(db)
        for company in company_list:
            address_list = \
                address.get_address_by_company(db, company.company_Id)
            job_count = job01.get_job_count_by_company(db, company.company_Id)
            if len(address_list) == 0:
                data.append([
                        company.company_Id, company.name,
                        '', '', '', '', '', job_count])
            else:
                for adr in address_list:
                    data.append([
                            company.company_Id, company.name,
                            adr.address_Id, adr.street, adr.city,
                            adr.state, adr.zip_code,
                            job_count])
# sort the data list by company.name and state
    data.sort(key=lambda x: (x[1], ('' if x[4] is None else x[4])))
    return data
