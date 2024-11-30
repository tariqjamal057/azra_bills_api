import asyncio
import sys

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from azra_bills_api.config.settings import settings
from azra_bills_api.conftest import (  # noqa: F401
    db_session,
    faker,
    mocker,
    override_session_dependency,
)
from azra_bills_api.core.dependencies import get_db_session
from main import admin_app
from main import app as main_app

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest_asyncio.fixture(scope="function")
async def async_client():
    admin_app.dependency_overrides[get_db_session] = override_session_dependency
    client = AsyncClient(
        transport=ASGITransport(app=main_app),
        base_url=settings.ADMIN_APP_BASE_URL,
        headers={},
    )
    async with client as test_client:
        yield test_client
