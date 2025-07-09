from typing import Protocol, Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from repository import RepositoryProtocol, SQLAlchemyRepositoryImpl
from .models import User


class UserRepositoryProtocol(RepositoryProtocol, Protocol):

    async def check_user_exists(self, session: AsyncSession, *args, **kwargs) -> bool:
        pass


class UserRepository(SQLAlchemyRepositoryImpl[User]):
    table = User

    async def check_user_exists(self, session: AsyncSession, *args, **kwargs) -> bool:
        query = select(self.table).filter_by(**kwargs)
        user = await session.scalar(query)
        return True if user else False


async def get_user_repository() -> UserRepositoryProtocol:
    return UserRepository()


UserRepositoryDep = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]
