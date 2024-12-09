"""This module contains the factory class for generating mock data for the SAASAdmin model.

It uses the BaseFactory class and polyfactory library to create realistic test data.
"""

from typing import Any, Dict

from azra_store_lmi_api.apps.admin.models.saas_admin import SAASAdmin
from azra_store_lmi_api.base_factory import BaseFactory


class SAASAdminFactory(BaseFactory):
    """Factory class for generating mock SAASAdmin instances.

    This class inherits from BaseFactory and provides methods to create test data for the SAASAdmin
    model.
    """

    model = SAASAdmin

    @classmethod
    def generate_mock_data(cls) -> Dict[str, Any]:
        """Generate mock data for the SAASAdmin model using the shared Faker instance.

        Returns:
            Dict[str, Any]: A dictionary containing mock data for SAASAdmin fields.
        """
        return {
            "first_name": cls.faker.first_name(),
            "last_name": cls.faker.last_name(),
            "email": cls.faker.email(),
            "username": cls.faker.user_name(),
            "phone_number": cls.faker.numerify("##########"),
            "password": cls.faker.password(length=12),
            "otp": cls.faker.numerify("######"),
            "opt_expire_at": cls.faker.future_datetime(),
            "is_active": cls.faker.boolean(),
        }
