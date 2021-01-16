"""

"""
import os

from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))
db_uri = 'sqlite:///jrm.db'
print(f"db uri: {db_uri}")

db = create_engine(db_uri, echo=True)
