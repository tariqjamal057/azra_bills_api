from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills.models.base import BaseModal

if TYPE_CHECKING:
    from azra_bills.models import Store


class User(BaseModal):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column(String(length=50))
    middle_name: Mapped[Optional[str]] = mapped_column(String(length=50))
    last_name: Mapped[str] = mapped_column(String(length=50))
    username: Mapped[str] = mapped_column(String(length=50))
    email: Mapped[str] = mapped_column(String(length=100))
    password: Mapped[str] = mapped_column(String(length=100))
    phone_country_code: Mapped[str] = mapped_column(String(length=5))
    phone_number: Mapped[str] = mapped_column(String(length=15))
    is_phone_number_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    user_type: Mapped[int] = mapped_column(Integer)

    stores: Mapped[list["Store"]] = relationship(back_populates="created_by")
