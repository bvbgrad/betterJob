"""
"""

import app.utils6L.utils6L as utils

import logging
import os
import PySimpleGUI as sg

from app.main.views import view_create_link_address
from app.model import db_session
from app.model.Company import Address, Company

from PySimpleGUI.PySimpleGUI import popup_scrolled

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)

NO_COMPANY_ADDRESS = 'No company address'


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


@utils.log_wrap
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
