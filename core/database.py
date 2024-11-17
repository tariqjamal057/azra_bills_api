"""Database Configuration and Base Models Module.

Provides core database functionality including:
- Async SQLAlchemy engine and session setup
- Custom naming conventions for database constraints
- Base model with timestamp tracking
- Schema management utilities

Key Components:
- AsyncSession: Configured session maker for async database operations
- Base: SQLAlchemy declarative base with naming conventions
- BaseModal: Abstract base class with created_at and updated_at fields
- set_tenant_schema: Utility for dynamic schema switching
- get_db_context: Context manager for getting the session
"""

from contextlib import asynccontextmanager
from typing import Optional

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncSession as SqlAlchemyAsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import settings
from core.constant import DB_PUBLIC_SCHEMA

async_engine = create_async_engine(settings.DATABASE_URL)

AsyncSession = sessionmaker(
    bind=async_engine,
    class_=SqlAlchemyAsyncSession,
    autocommit=False,
    autoflush=False,
)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))


async def set_tenant_schema(session: SqlAlchemyAsyncSession, *, schema: str):
    """Asynchronously checks if a given schema exists in the database session.

    Args:
        session (SqlAlchemyAsyncSession): The database session.
        schema (str): The name of the schema to check.
    """
    await session.execute(text(f"SET search_path TO {schema}"))


@asynccontextmanager
async def get_db_context(schema: Optional[str] = DB_PUBLIC_SCHEMA):
    """Get an SQLAlchemy database session.

    Creates a new session using the AsyncSession class provided by database.py.
    The session is closed after usage using a try/finally block.
    Args:
        schema (str): Tenant schema to use for the session. Default is DB_PUBLIC_SCHEMA.

    Returns:
        Session: The SQLAlchemy database session.
    """
    session = AsyncSession()
    await set_tenant_schema(session, schema)
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
