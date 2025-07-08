import asyncio

import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import AsyncClient, ASGITransport

from src.core import settings, db_helper
from src.main import app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_db():
    # startup
    assert settings.run.mode == "TEST"
    assert "_pytest" in settings.db.name or "_test" in settings.db.name

    yield db_helper.session_getter

    # shutdown
    await db_helper.dispose()


@pytest_asyncio.fixture(scope="package", autouse=True)
async def apply_migrations():
    alembic_cfg = Config(settings.files.alembic_ini)

    alembic_cfg.set_main_option("script_location", str(settings.files.alembic_dir))
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.db.POSTGRES_DSN))

    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

    yield

    await asyncio.to_thread(command.downgrade, alembic_cfg, "base")


@pytest_asyncio.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
        await client.aclose()
