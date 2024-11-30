"""This module provides a base factory class for handling model creation and relationship
generation.

It includes utilities for generating mock data, handling relationships, and creating model
instances asynchronously.
"""

from typing import Any, Dict, Optional

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession


class BaseFactory:
    """Base factory class for handling model creation and relationship generation."""

    # Initialize a single instance of Faker for use in all child factories
    faker = Faker()

    model = None

    @classmethod
    def generate_mock_data(cls) -> Dict[str, Any]:
        """Override this method in child factories to generate mock data for the model.

        Returns:
            Dict[str, Any]: A dictionary containing mock data for the model fields.
        """
        raise NotImplementedError

    @classmethod
    def relationship_factories(cls) -> Dict[str, Optional["BaseFactory"]]:
        """Override this method in child factories to specify related field factories.

        Returns:
            Dict[str, Optional["BaseFactory"]]: A dictionary mapping relationship names
            to their respective factories.
        """
        return {}

    @classmethod
    async def _handle_relationships(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Handle relationships and generate related model data if not provided.

        Args:
            kwargs (Dict[str, Any]): The keyword arguments containing relationship data.

        Returns:
            Dict[str, Any]: Updated keyword arguments with handled relationships.
        """
        relationship_factories = cls.relationship_factories()
        for relationship_name, factory in relationship_factories.items():
            if relationship_name not in kwargs or kwargs[relationship_name] is None:
                if factory is not None:
                    # If factory is provided, create related data
                    kwargs[relationship_name] = [await factory.create_async()]
                else:
                    # If no factory is provided for this relationship, assign an empty list
                    kwargs[relationship_name] = []

        return kwargs

    @classmethod
    async def create_async(
        cls, session: AsyncSession, refreshable: bool = False, **kwargs: Any
    ) -> Any:
        """Create and persist an instance asynchronously, handling relationships and other fields.

        Args:
            session (AsyncSession): The database session to use for persistence.
            refreshable (bool, optional): Whether to refresh the instance after creation.
            Defaults to False.
            **kwargs: Additional keyword arguments for instance creation.

        Returns:
            Any: The created model instance.
        """
        # Handle relationships before creating the instance
        kwargs = await cls._handle_relationships(kwargs)

        mock_data = cls.generate_mock_data() | kwargs
        mock_data.update(kwargs)
        instance = cls.model(**mock_data)
        session.add(instance)
        await session.commit()

        if refreshable:
            await session.refresh(instance)

        return instance

    @classmethod
    async def create_batch_async(
        cls, session: AsyncSession, count: int, refreshable: bool = False, **kwargs: Any
    ) -> list:
        """Create and persist multiple instances asynchronously.

        Args:
            session (AsyncSession): The database session to use for persistence.
            count (int): The number of instances to create.
            refreshable (bool, optional): Whether to refresh the instances after creation.
            Defaults to False.
            **kwargs: Additional keyword arguments for instance creation.

        Returns:
            list: A list of created model instances.
        """
        instances = []
        for _ in range(count):
            instance = await cls.create_async(session, refreshable=refreshable, **kwargs)
            instances.append(await session.refresh(instance) if refreshable else instance)
        return instances
