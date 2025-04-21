import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print("Loading database configuration for jobs")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_JOBS")
if SQLALCHEMY_DATABASE_URL is None:
    raise Exception("no url for partners database")


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)


def db_jobs():
    local_db = SessionLocal()
    try:
        yield local_db
    finally:
        local_db.close()
