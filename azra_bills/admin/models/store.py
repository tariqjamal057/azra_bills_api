from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ARRAY, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from azra_bills.models import BaseModalWithSoftDelete
from core.utils import ULIDGenerator

if TYPE_CHECKING:
    from azra_bills.admin.models import City, Country, Holiday, SAASAdmin, State


class Store(BaseModalWithSoftDelete):
    __tablename__ = "stores"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=expression.FunctionElement(ULIDGenerator.generate)
    )

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship()
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("states.id"))
    state: Mapped["State"] = relationship()
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("cities.id"))
    city: Mapped["City"] = relationship()
    parent_store_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("stores.id"))
    parent_store: Mapped["Store"] = relationship()
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("saas_admins.id"))
    created_by: Mapped["SAASAdmin"] = relationship(back_populates="stores")

    name: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    slogan: Mapped[Optional[str]] = mapped_column(String(length=100))
    address: Mapped[str] = mapped_column(String(length=255))
    postal_code: Mapped[str] = mapped_column(String(length=10))
    unique_indentifier: Mapped[Optional[str]] = mapped_column(String, unique=True)
    is_main_store: Mapped[bool] = mapped_column(Boolean, default=False)
    gst: Mapped[Optional[str]] = mapped_column(String(20))
    tin: Mapped[Optional[str]] = mapped_column(String(20))
    services: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    sub_services: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    has_online_booking: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_delivery_service: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_parking_facility: Mapped[Optional[bool]] = mapped_column(Boolean)
    has_wifi_facility: Mapped[Optional[bool]] = mapped_column(Boolean)

    contact_details: Mapped[List["StoreContactDetail"]] = relationship(back_populates="store")
    store_holidays: Mapped[List["Holiday"]] = relationship(back_populates="store")


class StoreContactDetail(BaseModalWithSoftDelete):
    __tablename__ = "store_contact_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    store_id: Mapped[str] = mapped_column(String, ForeignKey("stores.id"))
    store: Mapped[Store] = relationship(back_populates="contact_details")

    email: Mapped[str] = mapped_column(String(length=100))
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    phone_country_code: Mapped[str] = mapped_column(String(length=5))
    phone_number: Mapped[str] = mapped_column(String(length=15))
    is_phone_number_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    alternate_email: Mapped[Optional[str]] = mapped_column(String(length=100))
    is_alternate_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    alternate_phone_country_code: Mapped[Optional[str]] = mapped_column(String(length=5))
    alternate_phone_number: Mapped[Optional[str]] = mapped_column(String(length=15))
    is_alternate_phone_number_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    social_urls: Mapped[JSONB] = mapped_column(JSONB)
