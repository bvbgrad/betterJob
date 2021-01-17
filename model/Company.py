"""
    Database model and methods
    business object: Company 
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence, Integer, String, Column

Base = declarative_base()

class Company(Base):
    __tablename__ = 'Company'
    Id = Column(Integer, Sequence('company_id_seq'), primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return 'Company <{}>'.format(self.name)