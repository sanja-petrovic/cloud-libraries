from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

time.sleep(30)

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:postgres@{os.getenv("DB_HOST", "postgres")}:5432/{os.environ["DB"]}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
