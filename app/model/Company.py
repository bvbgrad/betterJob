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
