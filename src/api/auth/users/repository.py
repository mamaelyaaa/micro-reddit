from typing import Protocol, Annotated, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.dependencies import SessionDep
from .models import User


class UserRepositoryProtocol(Protocol):

    async def add_user(self, user_data: dict) -> int:
        pass

    async def get_user(self, *args, **kwargs) -> Optional[User]:
        pass

    async def check_user_exists(self, *args, **kwargs) -> bool:
        pass


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_data: dict) -> int:
        user = User(**user_data)
        self.session.add(user)
        await self.session.commit()
        return user.id

    async def get_user(self, *args, **kwargs) -> Optional[User]:
        query = select(User).filter_by(**kwargs)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def check_user_exists(self, *args, **kwargs) -> bool:
        query = select(User).filter_by(**kwargs)
        user = await self.session.scalar(query)
        return True if user else False


async def get_user_repository(session: SessionDep) -> UserRepositoryProtocol:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]
