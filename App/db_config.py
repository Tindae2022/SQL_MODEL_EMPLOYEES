import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

APP_ENV = os.getenv("APP_ENV", 'development')
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", 'postgres')
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", '12345')
DATABASE_HOST = os.getenv("DATABASE_HOST", 'localhost')
DATABASE_NAME = os.getenv("DATABASE_NAME", 'EMPLOYEESTEE')


SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()