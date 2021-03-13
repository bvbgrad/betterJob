"""
    Establish a  session factory for the database.

    There is normally only one session factory for the life of the application.
    The ORM’s “handle” to the database is the Session.

    See: https://docs.sqlalchemy.org/en/14/tutorial/engine.html
    "When we first set up the application, at the same level as our
    create_engine() statement, we define a Session class which will
    serve as a factory for new Session objects."
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_uri = 'sqlite:///jrm.db'

# echo=True displays SQL statements
db_engine = create_engine(db_uri, echo=False)
Session_db = sessionmaker(bind=db_engine)

Base = declarative_base()


@contextmanager
def db_session():
    """
    Provide a transactional scope around a series of operations.

    Set 'expire_on_commit=False' in order to mitigate lazy loading error
    Instance <object instance> is not bound to a Session;
      attribute refresh operation cannot proceed
      (Background on this error at: http://sqlalche.me/e/13/bhk3)
    """
    session = Session_db(expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
