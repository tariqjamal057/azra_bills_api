from sqlalchemy import DateTime, func
from sqlalchemy_easy_softdelete.mixin import generate_soft_delete_mixin_class


class SoftDeleteMixin(
    generate_soft_delete_mixin_class(
        column_name="deleted_at",
        deleted_at_column_type=DateTime(timezone=True),
        deleted_at_column_default=lambda: func.now(),
        generate_delete_method=True,
    )
):
    """Base Softdelete mixin for sqlalchemy models.

    It contain deleted_at field along with sqlalchemy model instance delete method
    """
