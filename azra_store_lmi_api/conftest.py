"""This module contains pytest fixtures and utility functions for setting up and tearing down test
databases, creating database sessions, and mocking functions for testing purposes."""

import os
from typing import Optional
from unittest.mock import MagicMock
from urllib.parse import urlparse

import pytest_asyncio
from faker import Faker
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from azra_store_lmi_api.core.enums import OrderByType
from azra_store_lmi_api.models import BaseModal

# Set up test database configuration
worker_id = os.getenv("PYTEST_XDIST_WORKER", "default")
test_db_name = f"azra_bills_test_db_{worker_id}"
db_url = urlparse(os.environ.get("DATABASE_URL", ""))
test_db_url = db_url._replace(path=f"/{test_db_name}")
postgres_db_url = db_url._replace(path="/postgres")

# Create async engines for test and postgres databases
async_test_engine = create_async_engine(test_db_url.geturl())
postgres_engine = create_async_engine(postgres_db_url.geturl(), isolation_level="AUTOCOMMIT")

async_session = sessionmaker(async_test_engine, class_=AsyncSession)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def engine():
    """Create a test database, set up tables, and tear down after tests.

    This fixture creates a test database, sets up the necessary tables,
    and yields the database engine. After all tests are complete, it
    drops the test database and disposes of the engines.

    Yields:
        sqlalchemy.ext.asyncio.AsyncEngine: The async engine for the test database.
    """
    async with postgres_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)"))
        await conn.execute(text(f"CREATE DATABASE {test_db_name}"))

    async with async_test_engine.begin() as conn:
        await conn.run_sync(BaseModal.metadata.create_all)

    yield async_test_engine

    async with postgres_engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE IF EXISTS {test_db_name} WITH (FORCE)"))

    await async_test_engine.dispose()
    await postgres_engine.dispose()


@pytest_asyncio.fixture
async def db_session():
    """Create and yield a database session for each test.

    This fixture creates a new database session for each test and
    yields it. The session is automatically closed after the test.

    Yields:
        sqlalchemy.ext.asyncio.AsyncSession: An async database session.
    """
    async with async_session() as session:
        yield session


async def override_session_dependency():
    """Create and yield an override database session.

    This asynchronous generator function creates a new database session
    using the async_session factory and yields it. The session is
    automatically closed after use.

    Yields:
        sqlalchemy.ext.asyncio.AsyncSession: An async database session.
    """
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def mocker(monkeypatch):
    """A fixture to mock functions and add return values or side effects.

    This fixture provides a function to easily mock other functions
    and set their return values or side effects for testing purposes.

    Args:
        monkeypatch (pytest.MonkeyPatch): The pytest monkeypatch fixture.

    Returns:
        Callable: A function to mock other functions.
    """

    async def _mocker(func_to_be_mocked, return_value=None, side_effect=None):
        """Mock a function and set its return value or side effect.

        Args:
            func_to_be_mocked (Callable): The function to be mocked.
            return_value (Any, optional): The return value for the mocked function.
            side_effect (Any, optional): The side effect for the mocked function.

        Returns:
            None
        """
        mock = MagicMock(return_value=return_value, side_effect=side_effect)
        monkeypatch.setattr(func_to_be_mocked, mock)

    return _mocker


@pytest_asyncio.fixture(scope="session")
def faker():
    """Fixture that provides a Faker instance for use in tests.

    Returns:
        function: A function that yields a configured Faker instance.
    """

    def _faker(max_value: Optional[int] = None):
        faker = Faker()
        faker.get_data_count = lambda: faker.random_int(1, 10 if not max_value else max_value)
        faker.get_order_by = lambda: faker.random_element(OrderByType.values())
        return faker

    return _faker
