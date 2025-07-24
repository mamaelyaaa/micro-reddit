from fastapi import status

from core.exceptions import AppException


class FollowNotFound(AppException):
    message: str = "Подписка не найдена"

    def __init__(self, message=message):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class FollowAlreadyExists(AppException):
    message: str = "Подписка уже существует"

    def __init__(self, message=message):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class SelfFollowError(AppException):
    message: str = "Нельзя подписаться на самого себя"

    def __init__(self, message=message):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)
