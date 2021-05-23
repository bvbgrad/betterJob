"""
"""

import app.utils6L.utils6L as utils

import logging
import os
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
    with db_session() as db:
        job01.add_job(db, job01)

    with db_session() as db:
        print(f"There are {job01.get_job_count(db)} jobs")
        for i, job in enumerate(job01.get_all_jobs(db), 1):
            print(f"{i:2} --- {job}")

    print(f"new job just added: {job01}")
