"""This module contains set of common dependencies that can be used over all apps."""

from fastapi import Query

from core.enums import OrderByType


async def paginator_query_params(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    order_by: OrderByType = Query(default=OrderByType.ASC.value),
):
    """Common dependency for the paginator query param."""
    return {"page": page, "size": size, "order_by": order_by}
