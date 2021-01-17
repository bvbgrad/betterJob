"""
    Establish a  session factory for the database.

    There is normally only one session factory for the life of the application.
    The ORM’s “handle” to the database is the Session. 

    See: https://docs.sqlalchemy.org/en/13/orm/tutorial.html
    "When we first set up the application, at the same level as our create_engine() statement, 
    we define a Session class which will serve as a factory for new Session objects."

"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
db_uri = 'sqlite:///jrm.db'

db_engine = create_engine(db_uri, echo=True)
Session = sessionmaker(bind=db_engine)
