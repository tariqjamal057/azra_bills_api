from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills_api.models import BaseModalWithSoftDelete

if TYPE_CHECKING:
    from azra_bills_api.admin.models import Store


class Holiday(BaseModalWithSoftDelete):
    __tablename__ = "holidays"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    store_id: Mapped[str] = mapped_column(String, ForeignKey("stores.id"))
    store: Mapped["Store"] = relationship(back_populates="store_holidays")
    created_by_id: Mapped[Optional[int]] = mapped_column(Integer)

    date: Mapped[Date] = mapped_column(Date)
    type: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(255))
    from_time: Mapped[Optional[Time]] = mapped_column(Time)
    to_time: Mapped[Optional[Time]] = mapped_column(Time)
