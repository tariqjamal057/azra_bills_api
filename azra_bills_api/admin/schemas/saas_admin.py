"""This module contains the saas admin module schemas."""

from pydantic import BaseModel, EmailStr, Field

from azra_bills_api.core.utils import PhoneNumberValidator


class SAASAdminRequest(BaseModel, PhoneNumberValidator):
    """Schema for creating a new SaaS admin.

    Attributes:
        username (str): The username of the admin. Must be between 3 and 50 characters long.
        first_name (str): The first name of the admin. Must be between 3 and 50 characters long.
        last_name (str): The last name of the admin. Must be between 3 and 50 characters long.
        email (str): The email address of the admin. Must match the EMAIL_PATTERN.
        phone_number (str): The phone number of the admin. Must match the PHONE_NUMBER_PATTERN.
    """

    username: str = Field(min_length=3, max_length=50, description="The username of the admin")
    first_name: str = Field(min_length=3, max_length=50, description="The first name of the admin")
    last_name: str = Field(min_length=3, max_length=50, description="The last name of the admin")
    email: EmailStr = Field(max_length=100, description="The email address of the admin")
    phone_number: str = Field(description="The phone number of the admin")


class ListSaaSAdmin(BaseModel):
    """Schema for listing SaaS admin details.

    Attributes:
        id (int): The unique identifier of the admin.
        first_name (str): The first name of the admin.
        last_name (str): The last name of the admin.
        email (str): The email address of the admin.
        phone_number (str): The phone number of the admin.
        is_active (bool): The active status of the admin account.
    """

    id: int = Field(description="The unique identifier of the admin")
    first_name: str = Field(description="The first name of the admin")
    last_name: str = Field(description="The last name of the admin")
    email: str = Field(description="The email address of the admin")
    phone_number: str = Field(description="The phone number of the admin")
    is_active: bool = Field(description="The active status of the admin account")
