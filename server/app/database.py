from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends
from models import *



sqlite_file_name='sales.db'
SQLALCHEMY_DATABASE_URL=f"sqlite:///./{sqlite_file_name}"
# DATABASE_URL = "postgresql+psycopg2://postgres:secure123@localhost:5432/salesdb"

# setup the engine for the database
engine=create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    # SQLModel.metadata.drop_all(engine)


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dpapi_connection, connection_record):
    cursor = dpapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()