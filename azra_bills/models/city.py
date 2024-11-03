from azra_bills.models.base import BaseModal

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, ForeignKey


class City(BaseModal):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    state_id: Mapped[int] = mapped_column(Integer, ForeignKey('states.id'))
    state: Mapped["State"] = relationship(back_populates="cities")

    name: Mapped[str] = mapped_column(String(100), nullable=False)

