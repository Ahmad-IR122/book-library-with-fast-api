from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from config.config import settings
from database import BaseModel
from models.book import Book
from models.member import Member
from models.borrowing import Borrowing


# This is the Alembic Config object.
# It gives access to values inside alembic.ini.
config = context.config


# Set the database URL dynamically from our application settings.
# This overrides the sqlalchemy.url value inside alembic.ini.
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)


# Configure Python logging using the alembic.ini file.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Alembic uses this metadata to detect changes in our models.
# Importing Book above ensures that the books table is registered
# inside BaseModel.metadata.
target_metadata = BaseModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode.

    In offline mode, Alembic does not create a real database connection.

    Instead, it uses the database URL and generates SQL statements
    that can be executed later.
    """

    # Get the database URL that was set above.
    url = config.get_main_option("sqlalchemy.url")

    # Configure Alembic for offline migration execution.
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Start a migration transaction.
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode.

    In online mode, Alembic creates a real connection
    to the database and applies migrations directly.
    """

    # Create a SQLAlchemy Engine using the Alembic configuration.
    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Open a connection to the database.
    with connectable.connect() as connection:

        # Configure Alembic to use the current database connection
        # and our SQLAlchemy model metadata.
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Start a migration transaction.
        with context.begin_transaction():
            context.run_migrations()


# Check which migration mode Alembic is running in.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()