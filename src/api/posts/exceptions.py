from fastapi import status

from core.exceptions import AppException


class PostNotFoundException(AppException):
    message: str = "Пост не найден"

    def __init__(self, message: str = message):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class PostAlreadyExist(AppException):
    message: str = "Пост с таким названием уже существует"

    def __init__(self, message: str = message):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)

