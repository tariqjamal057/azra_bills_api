from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import mapped_column

from azra_bills_api.mixins import SoftDeleteMixin
from core.database import Base


class BaseModal(Base, AsyncAttrs):
    """Base modal class for SQLAlchemy models.

    Contains common fields like created_at and updated_at.
    """

    __abstract__ = True

    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )


class BaseModalWithSoftDelete(BaseModal, SoftDeleteMixin):
    """Base modal class for SQLAlchemy models with soft delete functionality."""

    __abstract__ = True


class DeleteMixin:
    async def delete(self, session: AsyncSession):
        await session.delete(self)
