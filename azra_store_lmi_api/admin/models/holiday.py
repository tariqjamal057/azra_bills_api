"""This module contains the Holiday model."""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_store_lmi_api.core.utils import BaseEnum
from azra_store_lmi_api.models import BaseModalWithSoftDelete

if TYPE_CHECKING:
    from azra_store_lmi_api.admin.models import Store


class Holiday(BaseModalWithSoftDelete):
    """Represents a holiday in the database.

    This class defines the structure and relationships for the 'holidays' table.

    Attributes:
        id (int): The primary key of the holiday.

        store_id (str): The foreign key referencing the associated store.
        store (Store): The relationship to the Store model.
        created_by_id (int): The ID of the user who created the holiday.

        date (Date): The date of the holiday.
        type (int): The type of the holiday.
        reason (str): The reason for the holiday.
        from_time (Optional[Time]): The start time of the holiday.
        to_time (Optional[Time]): The end time of the holiday.

        store (Store): The relationship to the Store model.

    Inherits from:
        BaseModalWithSoftDelete: Provides common functionality for all models.
    """

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

    store: Mapped["Store"] = relationship(back_populates="store_holidays")


class HolidayType(BaseEnum):
    """Enumeration representing different types of holidays.

    Attributes:
        PUBLIC_HOLIDAY (int): Represents a public holiday (value: 10).
        STORE_HOLIDAY (int): Represents a store-specific holiday (value: 20).
    """

    PUBLIC_HOLIDAY = 10
    STORE_HOLIDAY = 20
