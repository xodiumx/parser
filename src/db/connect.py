# =================== Async connection =================== #

from crawls.settings import DATABASE

# from typing import AsyncGenerator

# from sqlalchemy import MetaData
# from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
#                                     create_async_engine)

# metadata = MetaData()

DB_USER = DATABASE['DB_USER']
DB_PASS = DATABASE['DB_PASS']
DB_HOST = DATABASE['DB_HOST']
DB_PORT = DATABASE['DB_PORT']
DB_NAME = DATABASE['DB_NAME']

# DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# engine = create_async_engine(DATABASE_URL)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session


# =================== Sync connection =================== #

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

metadata = MetaData()


DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(engine, expire_on_commit=True)


def get_session():
    """Getting a new session to connect to the database."""
    with Session() as session:
        yield session
