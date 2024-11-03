from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills.models.base import BaseModal

if TYPE_CHECKING:
    from azra_bills.models import City, Country


class State(BaseModal):
    __tablename__ = "states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.id"))
    country: Mapped["Country"] = relationship(back_populates="states")

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    state_code: Mapped[str] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(50))

    cities: Mapped[List["City"]] = relationship(back_populates="state")
