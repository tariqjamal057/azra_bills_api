"""Database Session Management Module.

This module provides database session management utilities with tenant schema support.
Key features:
- Async context manager for database sessions
- Automatic schema switching for multi-tenant support
- Built-in error handling and session cleanup
- Transaction rollback on exceptions

Usage:
    async with get_db_context("tenant_schema") as session:
        result = await session.execute(query)
        await session.commit()
"""

from contextlib import asynccontextmanager

from config.database import AsyncSession


@asynccontextmanager
async def get_db_context():
    """Get an SQLAlchemy database session.

    Creates a new session using the AsyncSession class provided by database.py.
    The session is closed after usage using a try/finally block.
    Args:
        tenant_schema (str): Tenant schema to use for the session. Default is DB_PUBLIC_SCHEMA.

    Returns:
        Session: The SQLAlchemy database session.
    """
    session = AsyncSession()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
