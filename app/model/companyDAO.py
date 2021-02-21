"""
"""

from sqlalchemy.orm import Session
from app.model import db_engine, Company

import app.utils6L.utils6L as utils
import logging
import os

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)


@utils.log_wrap
def add_company(company):
    logger.info(__name__ + f".add_company(): {company}")
    # TODO prevent adding duplicate companies

    company_list = get_company_list(company)
    print(f"company list: {company_list}")
    # if len(company_list) == 0:
    with Session(db_engine) as db:
        db.add(company)
        print(f"pending: {db.new}")
        db.commit()

    # return either an existing company list or
    # the newly created database entry
    # return company_list


@utils.log_wrap
def get_company_list(company):
    logger.info(__name__ + ".get_company_list()")

    # stmt = select(Company).where(Company.name == 'Ancestory')
    # stmt = select(Company)
    # print(stmt)
    with Session(db_engine) as db:
        # company_list = db.execute(stmt)
        company_list = db.execute(
            query(Company.name).filter_by(name='Ancestory')).scalar_one()
        for row in company_list:
            print(row)

    return company_list
