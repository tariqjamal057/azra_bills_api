"""This module contains set of common dependencies that can be used over all apps."""

from typing import AsyncGenerator, Literal

from fastapi import Query
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from azra_store_lmi_api.config.database import get_db_context
from azra_store_lmi_api.core.enums import OrderByType


async def paginator_query_params(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    order_by: Literal[*OrderByType.values()] = Query(default=OrderByType.ASC.value),
):
    """Common dependency for the paginator query param."""
    return {"page": page, "size": size, "order_by": asc if order_by == OrderByType.ASC else desc}


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Asynchronous generator that yields a database session.

    This function creates and yields an AsyncSession object within a database context.
    It should be used as a dependency in FastAPI route functions to manage database connections.

    Yields:
        AsyncSession: An asynchronous SQLAlchemy session object.

    Example:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_db_session)):
            # Use the db session here
            ...
    """
    async with get_db_context() as session:
        yield session
