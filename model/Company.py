"""
    Database model and methods
    business object: Company 
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy import Text, Integer, String, Column

from model import Base

class Company(Base):
    __tablename__ = 'company'
    Id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __repr__(self):
        return f"<Company(Id={self.Id!r}, name={self.name!r})>"
