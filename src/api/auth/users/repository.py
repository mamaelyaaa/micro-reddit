from typing import Protocol, Annotated, Optional

from fastapi import Depends
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.dependencies import SessionDep
from core.exceptions import BadRequestException
from .models import User
from .schemas import UserRegisterSchema, UserUpdateSchema, UserUpdatePartialSchema


class UserRepositoryProtocol(Protocol):

    async def add_user(self, user_data: UserRegisterSchema) -> int:
        pass

    async def get_user(self, *args, **kwargs) -> Optional[User]:
        pass

    async def check_user_exists(self, *args, **kwargs) -> bool:
        pass

    async def update_user(
        self,
        update_user_data: UserUpdateSchema | UserUpdatePartialSchema,
        partial: bool,
        *args,
        **kwargs,
    ) -> Optional[User]:
        pass


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_data: UserRegisterSchema) -> int:
        user = User(**user_data.model_dump())
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

    async def update_user(
        self,
        update_user_data: UserUpdateSchema | UserUpdatePartialSchema,
        partial: bool,
        *args,
        **kwargs,
    ) -> Optional[User]:
        user = await self.get_user(**kwargs)

        exists_email = await self.check_user_exists(email=update_user_data.email)
        if exists_email:
            raise BadRequestException("Данная почта уже зарегистрирована")

        exists_username = await self.check_user_exists(
            username=update_user_data.username
        )
        if exists_username:
            raise BadRequestException("Данный юзернейм уже занят")

        for key, value in update_user_data.model_dump(
            exclude_none=partial, exclude_unset=partial
        ).items():
            if not hasattr(user, key):
                raise
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user


async def get_user_repository(session: SessionDep) -> UserRepositoryProtocol:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepositoryProtocol, Depends(get_user_repository)]
