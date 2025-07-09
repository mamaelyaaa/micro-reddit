from typing import Protocol, TypeVar, Optional

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from core.exceptions import BadValidationException

Table = TypeVar("Table", bound=DeclarativeBase)


class RepositoryProtocol(Protocol):

    async def add_one(self, session: AsyncSession, data: dict) -> int:
        pass

    async def find_one(self, session: AsyncSession, *args, **kwargs):
        pass

    async def update_one(
        self, session: AsyncSession, update_data: dict, *args, **kwargs
    ):
        pass

    async def delete_one(self, *args, **kwargs) -> None:
        pass


class SQLAlchemyRepositoryImpl[Table]:
    table: type[Table]

    async def add_one(self, session: AsyncSession, data: dict) -> int:
        stmt = insert(self.table).values(**data).returning(self.table)
        res: Table = await session.scalar(stmt)
        await session.commit()
        return res.id

    async def find_one(self, session: AsyncSession, *args, **kwargs) -> Optional[Table]:
        query = select(self.table).filter_by(**kwargs)
        res = await session.execute(query)
        return res.scalar_one_or_none()

    async def update_one(
        self, session: AsyncSession, update_data: dict, *args, **kwargs
    ) -> Optional[Table]:
        entity = await self.find_one(session, *args, **kwargs)
        if not entity:
            return None

        for key, value in update_data.items():
            if not hasattr(entity, key):
                raise BadValidationException(f"Неизвестное поле для обновления: {key}")
            setattr(entity, key, value)

        await session.commit()
        await session.refresh(entity)
        return entity

    async def delete_one(self, *args, **kwargs) -> None:
        pass
