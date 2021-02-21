"""
    Database model and methods
    business object: Company
"""

from sqlalchemy import Column, Integer, String

from app.model import Base, Session_db


class Company(Base):
    __tablename__ = 'company'
    Id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return f"<Company(Id={self.Id!r}, name={self.name!r})>"

    def add_company(self, company):
        db = Session_db()
        result = db.query(Company).filter_by(name=company.name).count()
        if result > 0:
            raise ValueError(
                f"Company name <{company.name}> already in the database")
        else:
            db.add(company)
        db.commit()

    def get_company_count(self):
        db = Session_db()
        number_companies = db.query(Company).count()
        db.close()
        return number_companies

    def get_company_by_name(self, company_name):
        db = Session_db()
        company_list = db.query(Company).filter_by(name=company_name).all()
        db.close()
        return company_list

    def get_all_companies(self):
        db = Session_db()
        company_list = db.query(Company).all()
        db.close()
        return company_list
