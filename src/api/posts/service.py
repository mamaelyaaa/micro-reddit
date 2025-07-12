from typing import Protocol, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.auth.users.repository import UserRepositoryProtocol, UserRepositoryDep
from core.dependencies import SessionDep
from core.exceptions import BadRequestException, NotFoundException
from schemas import PaginationSchema
from .repository import PostRepositoryProtocol, PostRepositoryDep
from .schemas import (
    PostCreateSchema,
    PostReadSchema,
    PostUpdateSchema,
    PostUpdatePartialSchema,
)


class PostServiceProtocol(Protocol):

    async def create_post(self, user_id: int, post_data: PostCreateSchema) -> int:
        pass

    async def get_post_by_post_id(self, user_id: int, post_id: int) -> PostReadSchema:
        pass

    async def get_posts(
        self, user_id: int, pagination: PaginationSchema
    ) -> list[PostReadSchema]:
        pass

    async def update_post(
        self,
        user_id: int,
        post_id: int,
        post_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> PostReadSchema:
        pass

    async def delete_post(self, user_id: int, post_id: int) -> None:
        pass


class PostService:
    """Сервис постов авторизованного пользователя"""

    def __init__(
        self,
        session: AsyncSession,
        post_repo: PostRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
    ):
        self.session = session
        self.post_repo = post_repo
        self.user_repo = user_repo

    async def create_post(self, user_id: int, post_data: PostCreateSchema) -> int:
        exists_post = await self.post_repo.check_post_exists(
            user_id, title=post_data.title
        )
        if exists_post:
            raise BadRequestException("Пост с таким названием уже существует")

        post_id = await self.post_repo.create_user_post(
            user_id=user_id,
            post_data=post_data.model_dump(),
        )
        return post_id

    async def get_post_by_post_id(self, user_id: int, post_id: int) -> PostReadSchema:
        post = await self.post_repo.get_user_post(user_id=user_id, id=post_id)
        if not post:
            raise NotFoundException("Пост не найден")
        return PostReadSchema.model_validate(post)

    async def get_posts(
        self, user_id: int, pagination: PaginationSchema
    ) -> list[PostReadSchema]:
        posts = await self.post_repo.get_user_posts(
            user_id=user_id,
            limit=pagination.limit,
            offset=(pagination.page - 1) * pagination.limit,
        )
        return [PostReadSchema.model_validate(post) for post in posts]

    async def update_post(
        self,
        user_id: int,
        post_id: int,
        post_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> PostReadSchema:
        updated_post = await self.post_repo.update_post(
            user_id, post_id, update_data=post_data, partial=partial
        )
        if not updated_post:
            raise NotFoundException("Пост не найден")
        return PostReadSchema.model_validate(updated_post)

    async def delete_post(self, user_id: int, post_id: int) -> None:
        pass


async def get_posts_service(
    session: SessionDep,
    post_repo: PostRepositoryDep,
    user_repo: UserRepositoryDep,
) -> PostServiceProtocol:
    return PostService(session, post_repo, user_repo)


PostServiceDep = Annotated[PostServiceProtocol, Depends(get_posts_service)]
