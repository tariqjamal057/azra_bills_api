"""This module contains unit tests for the SAAS Admin functionality.

It includes tests for creating, listing, retrieving, updating, and deleting SAAS Admin records, as
well as error handling for various scenarios. These tests ensure the proper functioning of the SAAS
Admin API endpoints and related business logic.
"""

from unittest.mock import Mock

import pytest
from faker import Faker
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from azra_store_lmi_api.admin.models import SAASAdmin
from azra_store_lmi_api.admin.tests.factory import SAASAdminFactory
from azra_store_lmi_api.core.enums import OrderByType
from azra_store_lmi_api.test_utils import (
    assert_database_has,
    build_literal_error_message,
    generate_error_response,
    parse_validation_field,
)

BASE_ROUTE = "/saas-admins"

faker_ = Faker()

SAAS_ADMIN_SORT_BY_FIELDS = ["id", "email"]


@pytest.mark.asyncio
async def test_list_success(db_session: AsyncSession, async_client: AsyncClient, faker: Faker):
    """Test successful listing of SAAS admins with pagination and sorting."""
    total_saas_admin = await db_session.scalar(select(func.count(SAASAdmin.id)))
    saas_admin_count = faker().get_data_count()
    await SAASAdminFactory.create_batch_async(session=db_session, count=saas_admin_count)

    response = await async_client.get(
        f"{BASE_ROUTE}?sort_by=id&page=1&size=10&order_by={faker().get_order_by()}"
    )
    assert response.status_code == status.HTTP_200_OK
    response_content = response.json()
    assert response_content["total"] == total_saas_admin + saas_admin_count
    assert response_content["page"] == 1
    assert response_content["size"] == 10


list_param_errors_parameters = [
    pytest.param(
        {
            "sort_by": faker_.pystr(1, 5),
            "order_by": faker_.pystr(1, 5),
            "page": 1,
            "size": 10,
        },
        generate_error_response(
            [
                {
                    "field": "order_by",
                    "type": "literal_error",
                    "msg": build_literal_error_message(OrderByType.values()),
                },
                {
                    "field": "sort_by",
                    "type": "literal_error",
                    "msg": build_literal_error_message(SAAS_ADMIN_SORT_BY_FIELDS),
                },
            ]
        ),
        id="Invalid value for sort_by and order_by",
    ),
    pytest.param(
        {
            "order_by": faker_.random_element(OrderByType.values()),
            "sort_by": faker_.random_element(SAAS_ADMIN_SORT_BY_FIELDS),
            "page": 0,
            "size": 0,
        },
        generate_error_response(
            [
                {
                    "field": "page",
                    "type": "greater_than_equal",
                    "msg": "Input should be greater than or equal to 1",
                },
                {
                    "field": "size",
                    "type": "greater_than_equal",
                    "msg": "Input should be greater than or equal to 1",
                },
            ]
        ),
        id="Minimum length validation for page and size",
    ),
    pytest.param(
        {
            "order_by": faker_.random_element(OrderByType.values()),
            "sort_by": faker_.random_element(SAAS_ADMIN_SORT_BY_FIELDS),
            "page": 1,
            "size": faker_.random_int(1000, 1150),
        },
        generate_error_response(
            [
                {
                    "field": "size",
                    "type": "less_than_equal",
                    "msg": "Input should be less than or equal to 100",
                },
            ]
        ),
        id="Maximum length validation for size",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "params, error_response",
    list_param_errors_parameters,
)
async def test_list_param_errors(async_client: AsyncClient, params: dict, error_response: list):
    """Test error handling for invalid list parameters."""
    response = await async_client.get(
        f"{BASE_ROUTE}?sort_by={params['sort_by']}&page={params['page']}&size={params['size']}&order_by={params['order_by']}"
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert parse_validation_field(response.json()) == error_response


@pytest.mark.asyncio
async def test_list_server_error(async_client: AsyncClient, mocker):
    """Test server error response when listing SAAS admins fails."""
    await mocker("azra_store_lmi_api.admin.views.saas_admin.paginate", side_effect=Exception)
    response = await async_client.get(f"{BASE_ROUTE}?sort_by=id&page=1&size=10&order_by=asc")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Unable to list SAAS Admins, please try again later."}


create_success_params = [
    pytest.param(
        {
            "username": faker_.user_name(),
            "first_name": faker_.first_name(),
            "last_name": faker_.last_name(),
            "email": faker_.email(),
            "phone_number": faker_.numerify("##########"),
        },
        id="success param",
    )
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_create_succcess(
    db_session: AsyncSession, async_client: AsyncClient, faker: Faker, body: dict, monkeypatch
):
    """Test successful creation of a SAAS Admin."""
    mock_send_saas_admin_credentials = Mock()
    monkeypatch.setattr(
        "azra_store_lmi_api.admin.tasks.saas_admin.send_saas_admin_credentials.delay",
        mock_send_saas_admin_credentials,
    )
    response = await async_client.post(f"{BASE_ROUTE}", json=body)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"detail": "SAAS Admin has been created successfully."}
    await assert_database_has(db_session, SAASAdmin, [SAASAdmin.id], body)
    assert mock_send_saas_admin_credentials.assert_called_once


create_validation_errors = [
    pytest.param(
        {
            "username": faker_.user_name(),
            "first_name": faker_.first_name(),
            "last_name": faker_.last_name(),
            "email": faker_.email(),
            "phone_number": faker_.numerify("#########"),
        },
        generate_error_response(
            [
                {
                    "field": "phone_number",
                    "type": "value_error",
                    "msg": "Value error, Phone number must be exactly 10 digits long",
                },
            ]
        ),
        id="Invalid phone number length",
    ),
    pytest.param(
        {
            "username": faker_.user_name(),
            "first_name": faker_.first_name(),
            "last_name": faker_.last_name(),
            "email": faker_.pystr(1, 10),
            "phone_number": faker_.pystr(1, 6),
        },
        generate_error_response(
            [
                {
                    "field": "email",
                    "type": "value_error",
                    "msg": "value is not a valid email address: An email address must "
                    "have an @-sign.",
                },
                {
                    "field": "phone_number",
                    "type": "value_error",
                    "msg": "Value error, Phone number must contain only digits",
                },
            ]
        ),
        id="Invalid phone number and email",
    ),
    pytest.param(
        {
            "username": faker_.pystr(0, 2),
            "first_name": faker_.pystr(0, 2),
            "last_name": faker_.pystr(0, 2),
            "email": faker_.email(),
            "phone_number": faker_.numerify("##########"),
        },
        generate_error_response(
            [
                {
                    "field": "username",
                    "type": "string_too_short",
                    "msg": "String should have at least 3 characters",
                },
                {
                    "field": "first_name",
                    "type": "string_too_short",
                    "msg": "String should have at least 3 characters",
                },
                {
                    "field": "last_name",
                    "type": "string_too_short",
                    "msg": "String should have at least 3 characters",
                },
            ]
        ),
        id="Minimum length validation",
    ),
    pytest.param(
        {
            "username": faker_.pystr(1000, 1100),
            "first_name": faker_.pystr(1000, 1100),
            "last_name": faker_.pystr(1000, 1100),
            "email": faker_.email(),
            "phone_number": faker_.numerify("##########"),
        },
        generate_error_response(
            [
                {
                    "field": "username",
                    "type": "string_too_long",
                    "msg": "String should have at most 50 characters",
                },
                {
                    "field": "first_name",
                    "type": "string_too_long",
                    "msg": "String should have at most 50 characters",
                },
                {
                    "field": "last_name",
                    "type": "string_too_long",
                    "msg": "String should have at most 50 characters",
                },
            ]
        ),
        id="Minimum length validation",
    ),
    pytest.param(
        {
            "username": None,
            "first_name": None,
            "last_name": None,
            "email": None,
            "phone_number": None,
        },
        generate_error_response(
            [
                {
                    "field": "username",
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                },
                {
                    "field": "first_name",
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                },
                {
                    "field": "last_name",
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                },
                {
                    "field": "email",
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                },
                {
                    "field": "phone_number",
                    "type": "string_type",
                    "msg": "Input should be a valid string",
                },
            ]
        ),
        id="Invalid datatype",
    ),
    pytest.param(
        {},
        generate_error_response(
            [
                {
                    "field": "username",
                    "type": "missing",
                    "msg": "Field required",
                },
                {
                    "field": "first_name",
                    "type": "missing",
                    "msg": "Field required",
                },
                {
                    "field": "last_name",
                    "type": "missing",
                    "msg": "Field required",
                },
                {
                    "field": "email",
                    "type": "missing",
                    "msg": "Field required",
                },
                {
                    "field": "phone_number",
                    "type": "missing",
                    "msg": "Field required",
                },
            ]
        ),
        id="Required field validation",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body, error_response",
    create_validation_errors,
)
async def test_create_validation_errors(
    async_client: AsyncClient,
    body: dict,
    error_response: list,
):
    """Test that creating a SAAS Admin with invalid data returns a 422 with appropriate errors."""
    response = await async_client.post(f"{BASE_ROUTE}", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert parse_validation_field(response.json()) == error_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_create_already_exists_error(
    db_session: AsyncSession, async_client: AsyncClient, faker: Faker, body: dict
):
    """Test that creating a SAAS Admin with an existing email returns a 422 with an appropriate
    error.

    This test ensures that the API prevents creating a SAAS Admin with an email that is already
    associated with another SAAS Admin.
    """
    await SAASAdminFactory.create_async(session=db_session, email=body["email"])
    response = await async_client.post(f"{BASE_ROUTE}", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert parse_validation_field(response.json()) == generate_error_response(
        [
            {
                "field": "email",
                "type": "value_error",
                "msg": f"Value error, {body['email']} SAAS Admin already exists.",
            }
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_create_server_error(async_client: AsyncClient, mocker, body: dict):
    """Test that creating a SAAS Admin with a server error returns a 500 response with an
    appropriate error.

    This test ensures that the API returns a 500 status code with a user-friendly error message if
    an unexpected error occurs during the creation of a SAAS Admin.
    """
    await mocker("azra_store_lmi_api.admin.views.saas_admin.SAASAdmin", side_effect=Exception)
    response = await async_client.post(f"{BASE_ROUTE}", json=body)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Unable to create SAAS Admin, please try again later."}


@pytest.mark.asyncio
async def test_get_success(db_session: AsyncSession, async_client: AsyncClient):
    """Test that retrieving a SAAS Admin by ID returns a 200 response with the SAAS Admin details.

    This test ensures that the API returns a 200 status code with the SAAS Admin details if the
    SAAS Admin with the given ID exists.
    """
    saas_admin: SAASAdmin = await SAASAdminFactory.create_async(
        session=db_session, refreshable=True
    )
    response = await async_client.get(f"{BASE_ROUTE}/{saas_admin.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": saas_admin.id,
        "first_name": saas_admin.first_name,
        "last_name": saas_admin.last_name,
        "email": saas_admin.email,
        "phone_number": saas_admin.phone_number,
        "is_active": saas_admin.is_active,
        "created_at": saas_admin.created_at.isoformat(),
    }


@pytest.mark.asyncio
async def test_get_not_fount_error(
    async_client: AsyncClient,
):
    """Test that retrieving a SAAS Admin by ID with a non-existent ID returns a 404 response.

    This test ensures that the API returns a 404 status code with a user-friendly error message if
    the SAAS Admin with the given ID does not exist.
    """
    response = await async_client.get(f"{BASE_ROUTE}/0")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "SAAS Admin not found."}


@pytest.mark.asyncio
async def test_get_server_error(async_client: AsyncClient, mocker):
    """Test that retrieving a SAAS Admin by ID with a server error returns a 500 response.

    This test ensures that the API returns a 500 status code with a user-friendly error message if
    an unexpected error occurs during the retrieval of a SAAS Admin.
    """
    await mocker("azra_store_lmi_api.admin.views.saas_admin.SAASAdmin", side_effect=Exception)
    response = await async_client.get(f"{BASE_ROUTE}/0")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {
        "detail": "Unable to get details SAAS Admin, please try again later."
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_update_succcess(
    db_session: AsyncSession, async_client: AsyncClient, faker: Faker, body: dict, monkeypatch
):
    """Test that updating a SAAS Admin with valid data returns a 200 response with a user-friendly
    message.

    This test ensures that the API returns a 200 status code with a user-friendly message if the
    SAAS Admin with the given ID exists and valid update data is provided.
    """
    saas_admin: SAASAdmin = await SAASAdminFactory.create_async(
        session=db_session, refreshable=True
    )
    sass_admin_username = saas_admin.username
    response = await async_client.put(f"{BASE_ROUTE}/{saas_admin.id}", json=body)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "detail": f"{sass_admin_username} SAAS Admin has been updated successfully."
    }
    await assert_database_has(db_session, SAASAdmin, [SAASAdmin.id], body)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body, error_response",
    create_validation_errors,
)
async def test_update_validation_errors(
    async_client: AsyncClient,
    body: dict,
    error_response: list,
):
    """Test that updating a SAAS Admin with invalid data returns a 422 with appropriate errors.

    This test ensures that the API returns a 422 status code with appropriate errors if the SAAS
    Admin with the given ID exists and invalid update data is provided.
    """
    response = await async_client.put(f"{BASE_ROUTE}/{faker_.random_int()}", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert parse_validation_field(response.json()) == error_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_update_already_exists_error(
    db_session: AsyncSession, async_client: AsyncClient, body: dict
):
    """Test that updating a SAAS Admin with an existing email returns a 422 with an appropriate
    error.

    This test ensures that the API prevents updating a SAAS Admin's email to one that is already
    associated with another SAAS Admin, returning a 422 status code with a relevant error message.
    """
    saas_admin_user_1 = await SAASAdminFactory.create_async(session=db_session, refreshable=True)
    body["email"] = saas_admin_user_1.email
    saas_admin = await SAASAdminFactory.create_async(session=db_session, refreshable=True)
    response = await async_client.put(f"{BASE_ROUTE}/{saas_admin.id}", json=body)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert parse_validation_field(response.json()) == generate_error_response(
        [
            {
                "field": "email",
                "type": "value_error",
                "msg": f"Value error, {body['email']} SAAS Admin already exists.",
            }
        ]
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_update_not_found_error(async_client: AsyncClient, body: dict):
    """Test that updating a SAAS Admin with an invalid id returns a 404 with an appropriate error.

    This test ensures that the API prevents updating a SAAS Admin's information when the provided
    id is not associated with any SAAS Admin, returning a 404 status code with a relevant error
    message.
    """
    response = await async_client.put(f"{BASE_ROUTE}/0", json=body)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "SAAS Admin not found."}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    create_success_params,
)
async def test_update_server_error(async_client: AsyncClient, mocker, body: dict):
    """Test that updating a SAAS Admin with a valid request body returns a 500 internal server
    error.

    This test ensures that the API handles internal server errors gracefully and returns a 500
    status code with a relevant error message when updating a SAAS Admin's information fails due to
    an unexpected error.
    """
    await mocker("azra_store_lmi_api.admin.views.saas_admin.SAASAdmin", side_effect=Exception)
    response = await async_client.post(f"{BASE_ROUTE}/0", json=body)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Unable to update SAAS Admin, please try again later."}


@pytest.mark.asyncio
async def test_delete_success(db_session: AsyncSession, async_client: AsyncClient):
    """Test that deleting a SAAS Admin by ID returns a 200 response with a success message.

    This test ensures that the API returns a 200 status code with a confirmation message if the
    SAAS Admin with the given ID exists and is successfully deleted.
    """
    saas_admin = await SAASAdminFactory.create_async(session=db_session, refreshable=True)
    saas_admin_username = saas_admin.username
    response = await async_client.delete(f"{BASE_ROUTE}/{saas_admin.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "detail": f"{saas_admin_username} SAAS Admin has been deleted successfully."
    }


@pytest.mark.asyncio
async def test_delete_not_fount_error(
    async_client: AsyncClient,
):
    """Test that deleting a SAAS Admin with an invalid id returns a 404 with an appropriate error.

    This test ensures that the API prevents deleting a SAAS Admin's information when the provided
    id is not associated with any SAAS Admin, returning a 404 status code with a relevant error
    message.
    """
    response = await async_client.delete(f"{BASE_ROUTE}/0")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "SAAS Admin not found."}


@pytest.mark.asyncio
async def test_delete_server_error(async_client: AsyncClient, mocker):
    """Test that deleting a SAAS Admin with a server error returns a 500 response with an
    appropriate error.

    This test ensures that the API returns a 500 status code with a user-friendly error message if
    an unexpected error occurs during the deletion of a SAAS Admin.
    """
    await mocker("azra_store_lmi_api.admin.views.saas_admin.SAASAdmin", side_effect=Exception)
    response = await async_client.delete(f"{BASE_ROUTE}/0")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Unable to delete SAAS Admin, please try again later."}
