from asyncio import current_task
from re import M
from sys import meta_path
from tkinter import N
from typing import AsyncGenerator, Type

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .. import DATABASE_URI, SQLALCHEMY_ECHO, SQLALCHEMY_ISOLATION_LEVEL
from .base import hasReinitialize, normalizeUri

AsyncPostgreSQLEngine = create_async_engine(
    normalizeUri(DATABASE_URI),
    echo=SQLALCHEMY_ECHO,
    isolation_level=SQLALCHEMY_ISOLATION_LEVEL,
)
AsyncPostgreSQLScopedSession = async_scoped_session(
    async_sessionmaker(
        AsyncPostgreSQLEngine,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
        class_=AsyncSession,
    ),
    scopefunc=current_task,
)

async def initializePostgreDB(declarativeBase: Type[DeclarativeBase]):
    asyncEngine = AsyncPostgreSQLEngine
    metadata = declarativeBase.metadata

    async with asyncEngine.begin() as connection:
        if hasReinitialize(DATABASE_URI):
            await connection.run_sync(metadata.drop_all)

        await connection.run_sync(metadata.create_all)
    
    await asyncEngine.dispose()

def getAsyncPostgreSqlSession() -> AsyncSession:
    return AsyncPostgreSQLScopedSession

async def asyncPostgresqlSessionContextManager() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncPostgreSQLScopedSession() as session:
        yield session