from sqlalchemy import create_engine, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from unittest.mock import Mock
from os import getenv


SQLALCHEMY_DATABASE_URL = settings.db_connect_url

if not getenv("TEST"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=100,
        max_overflow=50,
        pool_timeout=30,
        pool_recycle=3600
    )
else:
    engine = Mock() 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def createTables():
    Base.metadata.create_all(bind=engine) 