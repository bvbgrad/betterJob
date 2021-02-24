"""
    Database model and methods
    business object: Company
"""

from sqlalchemy import Column, Integer, String

from app.model import Base


class Company(Base):
    __tablename__ = 'company'
    Id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return f"<Company(Id={self.Id!r}, name={self.name!r})>"

    def add_company(self, db, company):
        result = db.query(Company).filter_by(name=company.name).count()
        if result > 0:
            raise ValueError(
                f"Company name <{company.name}> already in the database")
        else:
            db.add(company)

    def delete_company(self, db, company):
        db.delete(company)

    def get_company_count(self, db):
        number_companies = db.query(Company).count()
        return number_companies

    def get_company_by_name(self, db, company_name):
        company_list = db.query(Company).filter_by(name=company_name).all()
        db.close()
        return company_list

    def get_all_companies(self, db):
        company_list = db.query(Company).all()
        return company_list


class Address(Base):
    __tablename__ = 'address'
    address_Id = Column(Integer, primary_key=True)
    street_address = Column(String(50))
    city = Column(String(20))
    state = Column(String(2))
    zip = Column(String(5))

    def __repr__(self):
        return f"< Address(Id={self.address_Id!r}, \
                street={self.street_address!r}, \
                city={self.city!r}, state={self.state!r}, \
                zip={self.zip!r}) >"
