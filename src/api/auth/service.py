from typing import Protocol, Annotated

from fastapi import Depends, Request, Response
from sqlalchemy.ext.asyncio.session import AsyncSession

from core import settings
from core.dependencies import SessionDep
from core.exceptions import (
    NotFoundException,
    ForbiddenException,
    BadRequestException,
)
from utils.security import verify_passwords
from .jwt.schemas import BearerResponseSchema
from .jwt.security import security
from .jwt.service import JWTService
from .users.repository import UserRepositoryProtocol, UserRepositoryDep
from .users.schemas import UserCreateSchema, UserReadSchema
from .users.service import UserService, UserServiceProtocol


class AuthServiceProtocol(UserServiceProtocol, Protocol):

    async def register_user(self, user_data: UserCreateSchema) -> int:
        pass

    async def login_user(
        self, user_data: UserCreateSchema, response: Response
    ) -> BearerResponseSchema:
        pass

    async def refresh_token(self, request: Request) -> BearerResponseSchema:
        pass

    async def get_current_user(self, request: Request) -> UserReadSchema:
        pass

    async def get_active_user(self, request: Request) -> UserReadSchema:
        pass

    async def get_superuser(self, request: Request) -> UserReadSchema:
        pass


class AuthService(UserService, JWTService):

    def __init__(self, session: AsyncSession, user_repo: UserRepositoryProtocol):
        super().__init__(session, user_repo)

    async def register_user(self, user_data: UserCreateSchema) -> int:
        user_id = await self.create_user(user_data)
        return user_id

    async def login_user(
        self, user_data: UserCreateSchema, response: Response
    ) -> BearerResponseSchema:
        user = await self._get_user_by(email=user_data.email)
        if not user:
            raise NotFoundException("Пользователь не найден")

        if not await verify_passwords(
            password=user_data.password,
            hash_pwd=user.password,
        ):
            raise BadRequestException("Неправильный пароль")

        access_token = self.create_access_token(
            uid=str(user.id),
            expiry=settings.jwt.access_expires,
        )
        refresh_token = self.create_refresh_token(
            uid=str(user.id),
            expiry=settings.jwt.refresh_expires,
        )
        security.set_refresh_cookies(
            token=refresh_token,
            max_age=settings.jwt.cookie_max_age,
            response=response,
        )

        return BearerResponseSchema(access_token=access_token)

    async def refresh_token(self, request: Request) -> BearerResponseSchema:
        refresh_token = await self.get_refresh_token_from_cookies(request)
        new_access = self.create_access_token(
            uid=str(refresh_token.sub), expiry=settings.jwt.access_expires
        )
        return BearerResponseSchema(access_token=new_access)

    async def get_current_user(self, request: Request) -> UserReadSchema:
        token = await self.get_access_token_from_headers(request)
        current_user = await self.user_repo.find_one(self.session, id=int(token.sub))
        return UserReadSchema.model_validate(current_user)

    async def get_active_user(self, request: Request) -> UserReadSchema:
        current_user = await self.get_current_user(request)
        if not current_user.is_active:
            raise ForbiddenException("Аккаунт деактивирован")
        return current_user

    async def get_superuser(self, request: Request) -> UserReadSchema:
        active_user = await self.get_active_user(request)
        if not active_user.is_superuser:
            raise ForbiddenException(
                "У вас недостаточно прав для доступа к этому ресурсу"
            )
        return active_user


async def get_auth_service(
    session: SessionDep,
    user_repo: UserRepositoryDep,
) -> AuthServiceProtocol:
    return AuthService(session, user_repo)


AuthServiceDep = Annotated[AuthServiceProtocol, Depends(get_auth_service)]
