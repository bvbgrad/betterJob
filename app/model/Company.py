"""
    Database model and methods
    business object: Company 
"""
from .base import Base
from sqlalchemy import Integer, String, Column

class Company(Base):
    __tablename__ = 'Company'
    Id = Column(Integer, primary_key=True)
    name = Column(String)
