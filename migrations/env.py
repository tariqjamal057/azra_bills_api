"""Alembic migration environment setup.

This module handles initializing and configuring the Alembic migration environment for the FastAPI
application.

It provides functions to run migrations and configure the migration context. The context is
configured by connecting to the database engine and targeting the metadata from models.py.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import text
from sqlalchemy.engine import Connection

from azra_bills_api.admin.models import *  # noqa: F403
from config.settings import settings
from core.database import Base, async_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


async def run_migrations_for_tenant(connection, schema_name):
    """Run migrations for a specific tenant schema.

    This function performs the following steps:
    1. Sets the search path to the specified schema.
    2. Creates or updates tenant-specific views.
    3. Runs migrations for the schema.

    Args:
        connection: The database connection to use for migrations.
        schema_name (str): The name of the tenant schema to migrate.
    """
    await set_search_path(connection, schema_name)
    await run_migrations_for_schema(connection)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """This allows running the migration context against a passed-in database connection instead of
    creating a new connection.

    Args:
        connection: The SQLAlchemy database connection to use for migrations.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def set_search_path(connection: Connection, schema: str) -> None:
    """Set the search path for the given schema."""
    await connection.execute(text(f"set search_path to {schema}"))
    await connection.commit()
    connection.dialect.default_schema_name = schema


async def run_migrations_for_schema(connection) -> None:
    """Run migrations for a specific schema."""
    await connection.run_sync(do_run_migrations)


async def fetch_db_schemas(connection) -> list:
    """Fetch the list of schemas from the database."""
    return (
        await connection.scalars(
            text(
                """SELECT schema_name FROM information_schema.schemata
                where schema_name not in ('pg_catalog', 'information_schema', 'pg_toast')"""
            )
        )
    ).all()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine and associate a connection with the context."""

    connectable = async_engine
    try:
        # Get the schema name from alembic upgrade command
        user_schema_name = context.get_x_argument(as_dictionary=True).get("tenant")
        async with connectable.connect() as connection:
            if user_schema_name is None:
                schema_list = await fetch_db_schemas(connection)
                if len(schema_list) > 0:
                    for schema in schema_list:
                        await run_migrations_for_tenant(connection, schema)
                else:
                    print("No schemas found in the database. Skipping migrations.")
            else:
                await run_migrations_for_tenant(connection, user_schema_name)
    except Exception as error:
        print(error)
    finally:
        await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
