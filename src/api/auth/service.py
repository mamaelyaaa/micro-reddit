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
from utils.security import verify_passwords, hash_password
from .jwt.repository import JWTRepositoryProtocol, JWTRepositoryDep
from .jwt.schemas import BearerResponseSchema
from .jwt.security import security
from .users.repository import UserRepositoryProtocol, UserRepositoryDep
from .users.schemas import UserReadSchema, UserRegisterSchema, UserLoginSchema


class AuthServiceProtocol(Protocol):

    async def register_user(self, user_data: UserRegisterSchema) -> int:
        pass

    async def login_user(
        self, user_data: UserLoginSchema, response: Response
    ) -> BearerResponseSchema:
        pass

    async def logout_user(self, request: Request, response: Response) -> None:
        pass

    async def refresh_token(self, request: Request) -> BearerResponseSchema:
        pass

    async def get_current_user(self, request: Request) -> UserReadSchema:
        pass

    async def get_active_user(self, request: Request) -> UserReadSchema:
        pass

    async def get_superuser(self, request: Request) -> UserReadSchema:
        pass


class AuthService:

    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepositoryProtocol,
        jwt_repo: JWTRepositoryProtocol,
    ):
        self.session = session
        self.user_repo = user_repo
        self.jwt_repo = jwt_repo

    async def register_user(self, user_data: UserRegisterSchema) -> int:
        exists_user_by_email = await self.user_repo.check_user_exists(
            email=user_data.email
        )
        if exists_user_by_email:
            raise BadRequestException("Данная почта уже зарегестрирована")

        exists_user_by_username = await self.user_repo.check_user_exists(
            username=user_data.username
        )
        if exists_user_by_username:
            raise BadRequestException("Данный юзернейм уже занят")

        if isinstance(user_data, UserRegisterSchema):
            data = UserRegisterSchema(
                username=user_data.username,
                email=user_data.email,
                password=await hash_password(user_data.password),
                is_superuser=user_data.is_superuser,
            )
        else:
            data = UserLoginSchema(
                username=user_data.username,
                email=user_data.email,
                password=await hash_password(user_data.password),
            )

        user = await self.user_repo.add_user(user_data=data.model_dump())
        return user

    async def login_user(
        self, user_data: UserLoginSchema, response: Response
    ) -> BearerResponseSchema:
        user = await self.user_repo.get_user(email=user_data.email)
        if not user:
            raise NotFoundException("Пользователь не найден")

        if not await verify_passwords(
            password=user_data.password,
            hash_pwd=user.password,
        ):
            raise BadRequestException("Неправильный пароль")

        access_token = self.jwt_repo.create_access_token(
            uid=str(user.id),
            expiry=settings.jwt.access_expires,
        )
        refresh_token = self.jwt_repo.create_refresh_token(
            uid=str(user.id),
            expiry=settings.jwt.refresh_expires,
        )
        security.set_refresh_cookies(
            token=refresh_token,
            max_age=settings.jwt.cookie_max_age,
            response=response,
        )

        return BearerResponseSchema(access_token=access_token)

    async def logout_user(self, request: Request, response: Response) -> None:
        await self.jwt_repo.get_access_token_from_headers(request, validate=False)
        security.unset_refresh_cookies(response)
        return

    async def refresh_token(self, request: Request) -> BearerResponseSchema:
        await self.jwt_repo.get_access_token_from_headers(request, validate=False)
        refresh_token = await self.jwt_repo.get_refresh_token_from_cookies(request)
        new_access = self.jwt_repo.create_access_token(
            uid=str(refresh_token.sub), expiry=settings.jwt.access_expires
        )
        return BearerResponseSchema(access_token=new_access)

    async def get_current_user(self, request: Request) -> UserReadSchema:
        token = await self.jwt_repo.get_access_token_from_headers(request)
        current_user = await self.user_repo.get_user(id=int(token.sub))
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
    jwt_repo: JWTRepositoryDep,
) -> AuthServiceProtocol:
    return AuthService(session, user_repo, jwt_repo)


AuthServiceDep = Annotated[AuthServiceProtocol, Depends(get_auth_service)]
