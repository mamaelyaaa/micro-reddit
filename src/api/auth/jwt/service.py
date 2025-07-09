from datetime import timedelta
from typing import Protocol

from authx import TokenPayload
from authx.exceptions import MissingTokenError, JWTDecodeError
from fastapi import Request

from core.exceptions import ForbiddenException, NotAuthorizedException
from .security import security


class JWTServiceProtocol(Protocol):

    def create_access_token(
        self, uid: str, expiry: timedelta, fresh: bool = False
    ) -> str:
        pass

    def create_refresh_token(self, uid: str, expiry: timedelta) -> str:
        pass

    async def get_access_token_from_headers(self, request: Request) -> TokenPayload:
        pass

    async def get_refresh_token_from_cookies(self, request: Request) -> TokenPayload:
        pass


class JWTService:
    @staticmethod
    def create_access_token(uid: str, expiry: timedelta, fresh: bool = False) -> str:
        access_token = security.create_access_token(uid=uid, fresh=fresh, expiry=expiry)
        return access_token

    @staticmethod
    def create_refresh_token(uid: str, expiry: timedelta) -> str:
        refresh_token = security.create_refresh_token(uid=uid, expiry=expiry)
        return refresh_token

    @staticmethod
    async def get_access_token_from_headers(request: Request) -> TokenPayload:
        try:
            token = await security.get_access_token_from_request(
                request, locations=["headers"]
            )
            payload = security.verify_token(token)
            return payload

        except MissingTokenError as e:
            raise ForbiddenException("Отсутствует токен доступа в запросе к платформе")
        except JWTDecodeError as e:
            raise NotAuthorizedException("Невалидный токен в запросе")

    @staticmethod
    async def get_refresh_token_from_cookies(request: Request) -> TokenPayload:
        try:
            token = await security.get_refresh_token_from_request(
                request, locations=["cookies"]
            )
            payload = security.verify_token(token, verify_csrf=False)
            return payload

        except MissingTokenError as e:
            raise ForbiddenException("Отсутствует токен обновления в запросе к платформе")

        except JWTDecodeError as e:
            raise NotAuthorizedException("Невалидный токен в запросе")
