"""This module contains the State model."""

from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills_api.models import BaseModal, DeleteMixin
from core.utils import BaseEnum

if TYPE_CHECKING:
    from azra_bills_api.admin.models import City, Country


class State(BaseModal, DeleteMixin):
    """Represents a state in the database.

    This class defines the structure and relationships for the 'states' table.

    Attributes
    id (int): The primary key of the state.

    country_id (int): The foreign key referencing the associated country.
    country (Country): The relationship to the Country model.

    name (str): The name of the state.
    state_code (str): The state code of the state.
    type (str): The type of the state.

    cities (List[City]): The relationship to the City model.

    Inherits from:
        BaseModal: Provides common functionality for all models.
        DeleteMixin: Adds soft delete capability to the model.
    """

    __tablename__ = "states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="states")

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    state_code: Mapped[str] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(50))

    cities: Mapped[List["City"]] = relationship(back_populates="state")


class StateTypeEnum(BaseEnum):
    """Enumeration class representing different types of states.

    Attributes:
        STATE (int): Represents a state.
        UNION_TERITORY (int): Represents a union territory.
    """

    STATE = 10
    UNION_TERITORY = 20
