"""
"""

import app.utils6L.utils6L as utils
import logging
import os

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)

from model import Session, Company
from sqlalchemy.orm import Query

# db = Session() retrieves a connection from the database engine connection pool
# This connection will be released when all changes are committed

@utils.log_wrap
def add_company(company):
    logger.info(__name__ + f".add_company(): {company}")
    #TODO prevent adding duplicate companies
    db = Session()
    db.add(company)
    db.commit()

    # company_list = get_company(company)
    # if len(company_list) == 0:
    #     db = Session()
    #     db.add(company)
    #     db.commit()
    #     company_list = get_company(company)

    # # return either an existing company list or the newly created database entry
    # return company_list


@utils.log_wrap
def get_company(company):
    logger.info(__name__ + f".get_company()")
    db = Session()

    # for instance in db.query(company).order_by(Company.Id):
    #     print(instance.Id, instance.name)

    company_list = db.query(Company).all()
    # company_list = db.query(Company).filter_by(name=company.name).all()
    return company_list
