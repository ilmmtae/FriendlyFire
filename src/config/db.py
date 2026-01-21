from dataclasses import dataclass

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from pydantic import PostgresDsn
from fastapi import FastAPI

from src.config.config import settings
from src.dependencies.database import RWSessionStub, RWDatabaseStub
from src.dependencies.stub import InjectContextManager, InjectStatic



@dataclass
class Postgres:
    engine: AsyncEngine
    async_session_maker: async_sessionmaker[AsyncSession]

    @classmethod
    def create(cls, dsn: PostgresDsn) -> "Postgres":
        engine: AsyncEngine = create_async_engine(
            f"{dsn}",
            pool_recycle=3600,
            pool_pre_ping=True,
            pool_size=50,
            max_overflow=30,
            pool_timeout=60,
        )
        async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
        )

        return cls(
            engine=engine,
            async_session_maker=async_session_maker,
        )

rw_database = Postgres.create(dsn=settings.SQLALCHEMY_DATABASE_URI)

def setup_database(app: FastAPI):
    app.dependency_overrides[RWSessionStub] = InjectContextManager(
        rw_database.async_session_maker
    )
    app.dependency_overrides[RWDatabaseStub] = InjectStatic(rw_database)
