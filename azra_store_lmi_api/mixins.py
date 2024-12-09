from sqlalchemy import DateTime, func
from sqlalchemy_easy_softdelete.mixin import generate_soft_delete_mixin_class


class SoftDeleteMixin(
    generate_soft_delete_mixin_class(
        deleted_field_name="deleted_at",
        deleted_field_type=DateTime(timezone=True),
        delete_method_default_value=lambda: func.now(),
        generate_delete_method=True,
    )
):
    """Base Softdelete mixin for sqlalchemy models.

    It contain deleted_at field along with sqlalchemy model instance delete method
    """
