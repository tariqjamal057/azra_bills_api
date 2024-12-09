"""This module contains the Country model."""

from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_store_lmi_api.models import BaseModalWithSoftDelete

if TYPE_CHECKING:
    from azra_store_lmi_api.apps.admin.models import State


class Country(BaseModalWithSoftDelete):
    """Represents a country in the database.

    This class defines the structure and relationships for the 'countries' table.

    Attributes
    id (int): The primary key of the country.

    name (str): The name of the country.
    numeric_code (str): The numeric code of the country.
    phone_code (str): The phone code of the country.
    capital (str): The capital of the country.
    currency (str): The currency of the country.
    currency_name (str): The name of the currency.
    currency_symbol (str): The symbol of the currency.
    region (str): The region of the country.
    region_id (int): The region ID of the country.
    subregion (str): The subregion of the country.
    subregion_id (int): The subregion ID of the country.

    states (List[State]): The relationship to the State model.

    Inherits from:
        BaseModalWithSoftDelete: Adds soft delete capability to the model.
    """

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

    states: Mapped[List["State"]] = relationship(back_populates="country")
