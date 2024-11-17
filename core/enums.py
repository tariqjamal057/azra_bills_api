"""This module contains set of enumeration that should used all over package."""

from enum import Enum

from sqlalchemy import asc, desc


class OrderByType(Enum):
    """Enumeration for the order_by type."""

    ASC = asc
    DESC = desc
