import logging
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from asyncpg.exceptions import ConnectionDoesNotExistError, InvalidPasswordError

from .config import settings
from .exceptions import UnavailibleService

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, url: str, echo: bool):
        self._engine = create_async_engine(url=url, echo=echo)
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    async def dispose(self) -> None:
        logger.debug("Подключение к базе данных разорвано")
        await self._engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
            except ConnectionDoesNotExistError as e:
                logger.error(str(e).capitalize())
                raise UnavailibleService(str(e).capitalize())


db_helper = Database(url=str(settings.db.POSTGRES_DSN), echo=bool(settings.db.echo))
