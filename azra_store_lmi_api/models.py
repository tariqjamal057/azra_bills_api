from sqlalchemy import DateTime, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import mapped_column

from azra_store_lmi_api.config.database import Base
from azra_store_lmi_api.mixins import SoftDeleteMixin


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
