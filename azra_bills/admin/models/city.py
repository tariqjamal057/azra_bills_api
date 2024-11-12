from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills.models import BaseModal, DeleteMixin

if TYPE_CHECKING:
    from azra_bills.admin.models import State


class City(BaseModal, DeleteMixin):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("states.id"))
    state: Mapped["State"] = relationship(back_populates="cities")

    name: Mapped[str] = mapped_column(String(100), nullable=False)
