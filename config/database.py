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
"""

from sqlalchemy import Column, DateTime, MetaData, func, text
from sqlalchemy.ext.asyncio import AsyncSession as SqlAlchemyAsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config.settings import settings

async_engine = create_async_engine(settings.DATABASE_URL)

AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=SqlAlchemyAsyncSession,
)

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base = declarative_base(metadata=MetaData(naming_convention=naming_convention))


async def set_tenant_schema(session: SqlAlchemyAsyncSession, schema_name: str):
    """Asynchronously checks if a given schema exists in the database session.

    Args:
        session (SqlAlchemyAsyncSession): The database session.
        schema_name (str): The name of the schema to check.
    """
    await session.execute(text(f"SET search_path TO {schema_name}"))


class BaseModal(Base):
    """Base modal class for SQLAlchemy models.

    Contains common fields like created_at and updated_at.
    """

    _abstract_ = True

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
