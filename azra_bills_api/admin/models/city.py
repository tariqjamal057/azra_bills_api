"""This module contains the City model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills_api.models import BaseModal, DeleteMixin

if TYPE_CHECKING:
    from azra_bills_api.admin.models import State


class City(BaseModal, DeleteMixin):
    """Represents a city in the database.

    This class defines the structure and relationships for the 'cities' table.

    Attributes:
        id (int): The primary key of the city.

        state_id (int): The foreign key referencing the associated state.
        state (State): The relationship to the State model.

        name (str): The name of the city.

    Inherits from:
        BaseModal: Provides common functionality for all models.
        DeleteMixin: Adds soft delete capability to the model.
    """

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("states.id"))
    state: Mapped["State"] = relationship(back_populates="cities")

    name: Mapped[str] = mapped_column(String(100), nullable=False)
