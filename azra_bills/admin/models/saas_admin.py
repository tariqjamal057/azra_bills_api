from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from azra_bills.models import BaseModal

if TYPE_CHECKING:
    from azra_bills.admin.models import Store


class SAASAdmin(BaseModal):
    __tablename__ = "saas_admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(10))
    password: Mapped[str] = mapped_column(String(50))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    stores: Mapped[list["Store"]] = relationship(back_populates="created_by")
