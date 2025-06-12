from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from ..core.config import Settings

engine = create_engine(Settings().DATABASE_URL)

Base = declarative_base()


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
