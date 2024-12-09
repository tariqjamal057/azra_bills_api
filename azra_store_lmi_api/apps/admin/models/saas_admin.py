"""This module contains the SAASAdmin model."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_store_lmi_api.apps.admin.tasks.saas_admin import send_saas_admin_credentials
from azra_store_lmi_api.core.security import AuthenticationMixin
from azra_store_lmi_api.models import BaseModalWithSoftDelete

if TYPE_CHECKING:
    from azra_store_lmi_api.apps.admin.models import Store


class SAASAdmin(BaseModalWithSoftDelete, AuthenticationMixin):
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
    hash_password: Mapped[str] = mapped_column("password", String(255))
    otp: Mapped[Optional[str]] = mapped_column(String(6))
    opt_expire_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    stores: Mapped[list["Store"]] = relationship(back_populates="created_by")

    @property
    def password(self):
        """Getter method for the password property.

        Returns:
            str: The hashed password of the admin user.
        """
        return self.hash_password

    @password.setter
    def password(self, password: str):
        """Setter method for the password property.

        This method hashes the provided plain text password before storing it.

        Args:
            password (str): The plain text password to be hashed and stored.
        """
        self.hash_password = self.get_hash_password(password)

    async def send_admin_credential(self, plain_password: str):
        """Asynchronously send admin credentials to the user.

        This method triggers a background task to send the admin's username,
        email, and plain text password to the user.

        Args:
            plain_password (str): The plain text password to be sent to the admin.

        Note:
            This method uses a delay mechanism, suggesting it's part of a task queue system.
        """
        send_saas_admin_credentials.delay(self.username, self.email, plain_password)
