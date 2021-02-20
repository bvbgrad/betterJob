"""
    Establish a  session factory for the database.

    There is normally only one session factory for the life of the application.
    The ORM’s “handle” to the database is the Session. 

    See: https://docs.sqlalchemy.org/en/14/tutorial/engine.html
    "When we first set up the application, at the same level as our create_engine() statement, 
    we define a Session class which will serve as a factory for new Session objects."

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

db_uri = 'sqlite:///jrm.db'

# echo=True displays SQL statements
# future=True invokes SQLAlchemy v2.0 features
db_engine = create_engine(db_uri, echo=True, future=True)

Base = declarative_base()
