"""This module contains the SAASAdmin model."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills_api.models import BaseModalWithSoftDelete

if TYPE_CHECKING:
    from azra_bills_api.admin.models import Store


class SAASAdmin(BaseModalWithSoftDelete):
    """Represents a SAAS admin in the database.

    This class defines the structure and relationships for the 'saas_admins' table.

    Attributes:
        id (int): The primary key of the SAAS admin.

        first_name (str): The first name of the SAAS admin.
        last_name (str): The last name of the SAAS admin.
        email (str): The email of the SAAS admin.
        phone_number (str): The phone number of the SAAS admin.
        password (str): The password of the SAAS admin.
        otp (Optional[str]): The OTP of the SAAS admin.
        opt_expire_at (Optional[DateTime]): The OTP expiration time of the SAAS admin.
        is_active (bool): Indicates whether the SAAS admin is active.

        stores (List[Store]): The relationship to the Store model.

    Inherits from:
        BaseModalWithSoftDelete: Provides common functionality for all models.
    """

    __tablename__ = "saas_admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(10))
    password: Mapped[str] = mapped_column(String(50))
    otp: Mapped[Optional[str]] = mapped_column(String(255))
    opt_expire_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    stores: Mapped[list["Store"]] = relationship(back_populates="created_by")
