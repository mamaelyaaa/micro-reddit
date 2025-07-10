from typing import Protocol

from sqlalchemy.ext.asyncio.session import AsyncSession

from core.exceptions import NotFoundException, BadRequestException
from utils.security import hash_password
from .models import User
from .repository import UserRepositoryProtocol
from .schemas import (
    UserUpdateSchema,
    UserUpdatePartialSchema,
    UserRegisterSchema,
    UserLoginSchema,
)


class UserServiceProtocol(Protocol):

    async def create_user(self, user_data: UserRegisterSchema | UserLoginSchema) -> int:
        pass

    async def get_user_by_user_id(self, user_id: int) -> User:
        pass

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdateSchema | UserUpdatePartialSchema,
        partial: bool,
    ) -> User:
        pass

    async def delete_user(self, user_id: int) -> None:
        pass


class UserService:

    def __init__(self, session: AsyncSession, user_repo: UserRepositoryProtocol):
        self.session = session
        self.user_repo = user_repo

    async def create_user(self, user_data: UserRegisterSchema | UserLoginSchema) -> int:
        exists_user = await self.user_repo.check_user_exists(
            session=self.session,
            email=user_data.email,
        )
        if exists_user:
            raise BadRequestException("Данная почта уже зарегестрирована")
        exists_user = await self.user_repo.check_user_exists(
            session=self.session,
            username=user_data.username,
        )
        if exists_user:
            raise BadRequestException("Данная юзернейм уже занят")

        if isinstance(user_data, UserRegisterSchema):
            data = UserRegisterSchema(username=user_data.username,
                email=user_data.email,
                password=await hash_password(user_data.password),
                is_superuser=user_data.is_superuser
            )
        else:
            data = UserLoginSchema(
                username=user_data.username,
                email=user_data.email,
                password=await hash_password(user_data.password),
            )

        user = await self.user_repo.add_one(self.session, data=data.model_dump())
        return user

    async def get_user_by_user_id(self, user_id: int) -> User:
        user = await self.user_repo.find_one(self.session, id=user_id)
        if not user:
            raise NotFoundException("Пользователь не найден")
        return user

    async def _get_user_by(self, *args, **kwargs) -> User:
        user = await self.user_repo.find_one(self.session, **kwargs)
        if not user:
            raise NotFoundException("Пользователь не найден")
        return user

    async def update_user(
        self,
        user_id: int,
        update_data: UserUpdateSchema | UserUpdatePartialSchema,
        partial: bool,
    ) -> User:
        updated_user = await self.user_repo.update_one(
            session=self.session,
            update_data=update_data.model_dump(
                exclude_unset=partial, exclude_none=partial
            ),
            id=user_id,
        )
        if not updated_user:
            raise NotFoundException("Пользователь не найден")

        return updated_user

    async def delete_user(self, user_id: int) -> None:
        pass
