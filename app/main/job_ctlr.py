"""
"""

from app.model.Company import Company
import app.utils6L.utils6L as utils

import logging
import os
import random
# import PySimpleGUI as sg

from app.model import db_session
from app.model.Job_Action import Job

logger_name = os.getenv("LOGGER_NAME")
logger = logging.getLogger(logger_name)


@utils.log_wrap
def get_job_data():
    logger.info(__name__ + ".get_job_data()")

    job01 = Job()
    job_data = []
    with db_session() as db:
        job_list = job01.get_all_jobs(db)
        for job in job_list:
            job_data.append(
                [job.job_Id, job.job_name, job.job_nbr,
                    job.priority, job.job_type, job.job_post_date,
                    job.job_expire_date, job.salary_min, job.salary_max,
                    job.company_IdFK]
                )
    return job_data


@utils.log_wrap
def add_job():
    logger.info(__name__ + ".add_job()")
    job01 = Job('test parameters', salary_min=110000, priority=5)
    company01 = Company()
    with db_session() as db:
        job01.add_job(db, job01)
    # bvb TODO temporary random assignment of a job to an existing company
        company_list = company01.get_all_companies(db)
        company_ids = []
        # create a set of existing company_Id's
        for company in company_list:
            company_ids.append(company.company_Id)
        for i, job in enumerate(job01.get_all_jobs(db), 1):
            random_company_Id = random.choice(company_ids)
            print(f"{i:2} --- company {random_company_Id} randomly assigned to job_Id = {job.job_Id}")
            job.company_IdFK = random_company_Id
            job.add_job(db, job)

    print(f"new job just added: {job01}")
