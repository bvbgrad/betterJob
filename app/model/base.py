"""
    Establish alembic base model
"""
import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# TODO if change database, have to change the db_uri accordingly
db_uri = 'sqlite:///jrm.db'


def get_base():

    print(f"get_base() database: {db_uri}")
    return {'base': Base, 'sqlalchemy_url': db_uri}
