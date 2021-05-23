"""
    Database model and methods
    business object: Job Actions
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Date

from app.model import Base

from datetime import date


class Job(Base):
    __tablename__ = 'job'
    job_Id = Column(Integer, primary_key=True)
    job_name = Column(String(50))
    job_nbr = Column(String(30))
    # bvb TODO change priority to status  # active, fav1-5, inactive
    priority = Column(String(10))
    job_type = Column(String(10))
    job_post_date = Column(Date())
    job_expire_date = Column(Date())
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    company_IdFK = Column(Integer, ForeignKey('company.company_Id'))

    def __init__(
        self, job_name=None, job_nbr=None, priority=3, job_type=None,
            job_post_date=None, job_expire_date=None,
            salary_min=0, salary_max=None, company_IdFK=0):

        self.job_name = job_name
        self.job_nbr = job_nbr
        self.priority = priority
        self.job_type = job_type

        if job_post_date is None:
            self.job_post_date = date.today()
        else:
            self.job_post_date

        self.job_expire_date = job_expire_date
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.company_IdFK = company_IdFK

    def __repr__(self):
        return f"Job(Id={self.job_Id!r}, name={self.job_name!r}, " +\
            f"job_nbr={self.job_nbr}, priority={self.priority}, " +\
            f"job_type={self.job_type}, " +\
            f"job_post_date={self.job_post_date}, " +\
            f"job_expire_date={self.job_expire_date}, " +\
            f"salary_min={self.salary_min}, salary_max={self.salary_max}, " +\
            f"company_IdFK={self.company_IdFK})"

    def add_job(self, db, job):
        db.add(job)

    def get_job_count(self, db):
        number_jobs = db.query(Job).count()
        return number_jobs

    def get_job_count_by_company(self, db, company_id):
        return db.query(Job).filter_by(company_IdFK=company_id).count()

    def get_job_by_company(self, db, company_id):
        return db.query(Job).filter_by(company_IdFK=company_id).all()

    def get_all_jobs(self, db):
        job_list = db.query(Job).all()
        return job_list
