from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills.models.base import BaseModal
from core.utils import uuid_generator

if TYPE_CHECKING:
    from azra_bills.models import City, Country, State, User


class Store(BaseModal):
    __tablename__ = "stores"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default_factory=uuid_generator
    )

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"))
    country: Mapped["Country"]
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("states.id"))
    state: Mapped["State"]
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"))
    city: Mapped["City"]
    parent_store_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stores.uuid")
    )
    parent_store: Mapped["Store"]
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_by: Mapped["User"] = relationship(back_populates="stores")

    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    slogan: Mapped[Optional[str]] = mapped_column(String(length=100))
    email: Mapped[str] = mapped_column(String(length=100))
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    phone_country_code: Mapped[str] = mapped_column(String(length=5))
    phone_number: Mapped[str] = mapped_column(String(length=15))
    is_phone_number_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    address: Mapped[str] = mapped_column(String(length=255))
    postal_code: Mapped[str] = mapped_column(String(length=10))
    unique_indentifier: Mapped[Optional[str]] = mapped_column(String, unique=True)
    is_main_store: Mapped[bool] = mapped_column(Boolean, default=False)
    type: Mapped[int] = mapped_column(Integer)
    gst: Mapped[Optional[str]] = mapped_column(String(20))
    tin: Mapped[Optional[str]] = mapped_column(String(20))
