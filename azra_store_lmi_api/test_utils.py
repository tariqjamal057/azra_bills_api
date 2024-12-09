"""Module contains utility class/function to be used in testcases."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from azra_store_lmi_api.models import BaseModal


def build_literal_error_message(valid_columns: list):
    """Common function to build error message for literal validation failure."""
    valid_columns_str = "', '".join(valid_columns[:-1]) + "' or '" + valid_columns[-1] + "'"
    return f"Input should be '{valid_columns_str}"


def parse_validation_field(response: Any):
    """Gets the Pydantic error message and returns the required message."""
    error_response = []
    for error in response["detail"]:
        try:
            error_field = error["loc"][-1]
        except IndexError:
            error_field = error["loc"][0]
        error_type = error["type"]
        error_desc = error["msg"]
        error_response.append({"field": error_field, "type": error_type, "msg": error_desc})
    return error_response


def generate_error_response(expected_errors: list):
    """Generates a response based on the given error type, field and message."""
    return_response = []
    for error in expected_errors:
        error_instance = {}
        error_instance["field"] = error["field"]
        error_instance["type"] = error["type"]
        error_instance["msg"] = error["msg"]
        return_response.append(error_instance)
    return return_response


async def assert_database_has(
    session: AsyncSession, model: type[BaseModal], columns: list, filters: dict
) -> None:
    """This function checks whether the DB has the data which we have created or manipulated."""
    query = select(*columns)
    for key, value in filters.items():
        query = query.filter(getattr(model, key) == value)
    instance = await session.scalar(query)
    assert instance != []


async def assert_database_not_has(
    session: AsyncSession, model: type[BaseModal], columns: list, filters: dict
) -> None:
    """This function checks whether the data we desired to delete, has been deleted ot not."""
    query = select(*columns)
    for key, value in filters.items():
        query = query.filter(getattr(model, key) == value)
    instance = await session.scalar(query)
    assert instance == []
