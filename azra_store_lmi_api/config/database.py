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
from typing import AsyncGenerator

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from azra_store_lmi_api.config.settings import settings

async_engine = create_async_engine(settings.DATABASE_URL)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))


async def set_tenant_schema(session: AsyncSession, *, schema: str):
    """Asynchronously checks if a given schema exists in the database session.

    Args:
        session (AsyncSession): The database session.
        schema (str): The name of the schema to check.
    """
    await session.execute(text(f"SET search_path TO {schema}"))


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """Asynchronous context manager for database session handling.

    Yields:
        AsyncSession: An asynchronous database session.

    Raises:
        Exception: Any exception that occurs during database operations.

    Notes:
        - The session is automatically closed when exiting the context.
        - If an exception occurs, the session is rolled back before being closed.
    """
    session = async_session()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
