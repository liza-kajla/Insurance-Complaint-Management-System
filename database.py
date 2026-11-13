from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:98158@127.0.0.1:5432/insurance_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind = engine)

Base = declarative_base()

# create dependency function
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
