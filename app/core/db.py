import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = os.getenv('POSTGRES_URL')

postgres_engine = create_engine(SQLALCHEMY_DATABASE_URL)
PostgresSessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=postgres_engine)
Base = declarative_base()


def get_postgres_session():
    with Session(postgres_engine) as session:
        yield session
