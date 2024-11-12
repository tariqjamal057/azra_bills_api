from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills.models import BaseModal, DeleteMixin

if TYPE_CHECKING:
    from azra_bills.admin.models import State


class Country(BaseModal, DeleteMixin):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String(100))
    numeric_code: Mapped[str] = mapped_column(String(3))
    phone_code: Mapped[str] = mapped_column(String(10))
    capital: Mapped[str] = mapped_column(String(100))
    currency: Mapped[str] = mapped_column(String(3))
    currency_name: Mapped[str] = mapped_column(String(50))
    currency_symbol: Mapped[str] = mapped_column(String(5))
    region: Mapped[str] = mapped_column(String(50))
    region_id: Mapped[int] = mapped_column(Integer)
    subregion: Mapped[str] = mapped_column(String(50))
    subregion_id: Mapped[int] = mapped_column(Integer)
    nationality: Mapped[str] = mapped_column(String(50))
    is_operational: Mapped[bool] = mapped_column(Boolean, default=False)

    states: Mapped[List["State"]] = relationship(back_populates="country")
