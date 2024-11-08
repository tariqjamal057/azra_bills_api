import asyncio
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection

from core.database import Base, async_engine

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

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


async def set_migration_db_schema(connection: Connection, schema: str) -> None:
    """Set the database schema for the migration."""
    await connection.execute(f"SET search_path TO {schema}")


async def get_db_schemas(connection: Connection) -> list[str]:
    """Get the list of schemas from the database."""
    schemas = (
        await connection.execute(
            "SELECT schema_name FROM information_schema.schemata "
            "where schema_name not in ('pg_catalog', 'information_schema', 'pg_toast')"
        )
    ).all()
    return [schema[0] for schema in schemas]


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
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine and associate a connection with the context."""

    async_connection = async_engine
    try:
        custom_schema = context.get_x_argument(as_dictionary=True).get("tenant")
        async with async_connection.connect() as connection:
            if custom_schema:
                await set_migration_db_schema(connection, custom_schema)
                await connection.run_sync(do_run_migrations)
            else:
                schemas = await get_db_schemas(connection)
                if not schemas:
                    print("No schema found in the database. Skipping migrations.")
                else:
                    for schema in schemas:
                        await set_migration_db_schema(connection, schema)
                        await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(e)
    finally:
        await async_connection.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
