
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# this is the Alembic Config object, which provides access to values within the .ini file
config = context.config

# Override DB URL from env if present
db_url = os.getenv("DATABASE_URL")
if db_url:
    # Alembic uses sync drivers; map async URLs to sync where possible
    if db_url.startswith("postgresql+asyncpg://"):
        db_url = db_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://")
    config.set_main_option("sqlalchemy.url", db_url)

fileConfig(config.config_file_name)  # type: ignore

# add your model's MetaData object here for 'autogenerate' support
from app.models import Base  # noqa
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
