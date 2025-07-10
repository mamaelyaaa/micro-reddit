from typing import Protocol, Annotated

from fastapi import Depends

from repository import RepositoryProtocol, SQLAlchemyRepositoryImpl
from .models import Post


class PostRepositoryProtocol(RepositoryProtocol, Protocol):
    pass


class PostRepository(SQLAlchemyRepositoryImpl[Post]):
    table = Post



async def get_posts_repository() -> PostRepositoryProtocol:
    return PostRepository()


PostRepositoryDep = Annotated[PostRepositoryProtocol, Depends(get_posts_repository)]
