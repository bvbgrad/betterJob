"""
    Database model and methods
    business object: Company
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.model import Base


class Company(Base):
    __tablename__ = 'company'
    company_Id = Column(Integer, primary_key=True)
    # bvb TODO add status = Column (String(10))  # active, fav1-5, inactive
    name = Column(String(30))
    address = relationship("Address")

    def __repr__(self):
        return f"Company(Id={self.company_Id!r}, name={self.name!r})"

    def add_company(self, db, company):
        result = db.query(Company).filter_by(name=company.name).count()
        if result > 0:
            # A 'result > 0' ensures no duplicate company names
            # bvb TODO Make company name column a unique index and not null
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
        company = db.query(Company).filter_by(name=company_name).first()
        return company

    def get_all_companies(self, db):
        company_list = db.query(Company).all()
        return company_list


class Address(Base):
    __tablename__ = 'address'
    address_Id = Column(Integer, primary_key=True)
    street = Column(String(50))
    city = Column(String(30))
    state = Column(String(2))
    zip_code = Column(String(5))
    company_IdFK = Column(Integer, ForeignKey('company.company_Id'))

    def __init__(self, street=None, city=None, state=None, zip_code=None):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self):
        return f"Address(Id={self.address_Id!r}, street={self.street!r}, " +\
            f"city={self.city!r}, state={self.state!r}, " +\
            f"zip code={self.zip_code!r})"

    def __eq__(self, other):
        if (isinstance(other, Address)):
            return self.street == other.street and \
                self.city == other.city and \
                self.state == other.state and \
                self.zip_code == other.zip_code
        return False

    def add_address(self, db, address):
        db.add(address)

    def get_address_count(self, db):
        number_addresses = db.query(Address).count()
        return number_addresses

    def get_address_list(self, db):
        address_list = db.query(Address).all()
        return address_list

    def get_address_by_company(self, db, company_id):
        return db.query(Address).filter_by(company_IdFK=company_id).all()

    def delete_address(self, db, address):
        db.delete(address)

    def delete_self(self, db):
        db.delete(self)
