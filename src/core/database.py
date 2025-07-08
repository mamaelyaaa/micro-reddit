from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from .config import settings


class Database:
    def __init__(self, url: str, echo: bool):
        self._engine = create_async_engine(url=url, echo=echo)
        self._session_factory = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    async def dispose(self) -> None:
        await self._engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            yield session


db_helper = Database(url=str(settings.db.POSTGRES_DSN), echo=bool(settings.db.echo))
