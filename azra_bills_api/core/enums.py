"""This module contains set of enumeration that should used all over package."""

from azra_bills_api.core.utils import BaseEnum


class OrderByType(BaseEnum):
    """Enumeration for the order_by type."""

    ASC = "asc"
    DESC = "desc"