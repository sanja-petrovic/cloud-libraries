from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os
import time


def wait_for_db(db_uri):
    _local_engine = create_engine(db_uri)

    _LocalSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=_local_engine
    )

    up = False
    while not up:
        try:
            db_session = _LocalSessionLocal()
            db_session.execute(text("SELECT 1"))
            db_session.commit()
        except Exception as err:
            print(f"Connection error: {err}")
            up = False
        else:
            up = True

        time.sleep(2)


SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:postgres@{os.getenv("DB_HOST", "postgres")}:5432/{os.environ["DB"]}'
wait_for_db(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
