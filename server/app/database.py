from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import Annotated
from fastapi import Depends
from models import *
from dotenv import load_dotenv
import os

load_dotenv()


# sqlite_file_name='sales.db'
# SQLALCHEMY_DATABASE_URL=f"sqlite:///./{sqlite_file_name}"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://salesuser:Secure123@localhost:5432/salesdb"

# DATABASE_URL = os.getenv("DATABASE_URL")
# setup the engine for the database
# engine=create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
engine=create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False, future=True, pool_size=20, max_overflow=40, pool_timeout=60)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


    # SQLModel.metadata.drop_all(engine)


# @event.listens_for(Engine, "connect")
# async def enable_sqlite_foreign_keys(dpapi_connection, connection_record):
#     cursor = await dpapi_connection.cursor()
#     await cursor.execute("PRAGMA foreign_keys=ON")
#     await cursor.close()