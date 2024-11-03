

from azra_bills.models.base import BaseModal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from typing import List


class State(BaseModal):
    __tablename__ = 'states'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    country_id: Mapped[int] = mapped_column(Integer, ForeignKey('countries.id'))
    country: Mapped["Country"] = relationship( back_populates="states")

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    state_code: Mapped[str] = mapped_column(String(10))
    type: Mapped[str] = mapped_column(String(50))

    cities: Mapped[List["City"]] = relationship(back_populates="state")
