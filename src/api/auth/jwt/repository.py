import logging
from datetime import timedelta
from typing import Protocol, Annotated

from authx import TokenPayload, RequestToken
from authx.exceptions import MissingTokenError, JWTDecodeError
from fastapi import Request, Depends

from core.exceptions import ForbiddenException, NotAuthorizedException
from .security import security

logger = logging.getLogger("jwt_repo")


class JWTRepositoryProtocol(Protocol):

    def create_access_token(
        self, uid: str, expiry: timedelta, fresh: bool = False
    ) -> str:
        pass

    def create_refresh_token(self, uid: str, expiry: timedelta) -> str:
        pass

    async def get_access_token_from_headers(
        self, request: Request, validate: bool = True
    ) -> TokenPayload | RequestToken:
        pass

    async def get_refresh_token_from_cookies(
        self, request: Request, validate: bool = True
    ) -> TokenPayload | RequestToken:
        pass


class JWTRepository:

    @staticmethod
    def create_access_token(uid: str, expiry: timedelta, fresh: bool = False) -> str:
        logger.debug("Создаем токен доступа...")
        access_token = security.create_access_token(uid=uid, fresh=fresh, expiry=expiry)
        return access_token

    @staticmethod
    def create_refresh_token(uid: str, expiry: timedelta) -> str:
        logger.debug("Создаем токен обновления...")
        refresh_token = security.create_refresh_token(uid=uid, expiry=expiry)
        return refresh_token

    @staticmethod
    async def get_access_token_from_headers(
        request: Request, validate: bool = True
    ) -> TokenPayload | RequestToken:
        try:
            token = await security.get_access_token_from_request(
                request, locations=["headers"]
            )
            if validate:
                payload = security.verify_token(token)
                return payload
            return token

        except MissingTokenError:
            msg = "Отсутствует токен доступа в запросе к платформе"
            logger.error(msg)
            raise ForbiddenException(msg)

        except JWTDecodeError:
            msg = "Невалидный токен в запросе"
            logger.error(msg)
            raise NotAuthorizedException(msg)

    @staticmethod
    async def get_refresh_token_from_cookies(
        request: Request, validate: bool = True
    ) -> TokenPayload | RequestToken:
        try:
            token = await security.get_refresh_token_from_request(
                request, locations=["cookies"]
            )
            if validate:
                payload = security.verify_token(token, verify_csrf=False)
                return payload
            return token

        except MissingTokenError:
            msg = "Отсутствует токен обновления в запросе к платформе"
            logger.error(msg)
            raise ForbiddenException(msg)

        except JWTDecodeError:
            msg = "Невалидный токен в запросе"
            logger.error(msg)
            raise NotAuthorizedException(msg)


async def get_jwt_repository() -> JWTRepositoryProtocol:
    return JWTRepository()


JWTRepositoryDep = Annotated[JWTRepositoryProtocol, Depends(get_jwt_repository)]
