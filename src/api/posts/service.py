import logging
from typing import Protocol, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.auth.users.repository import UserRepositoryProtocol, UserRepositoryDep
from core.dependencies import SessionDep
from schemas import PaginationSchema
from .exceptions import PostNotFoundException, PostAlreadyExist
from .repository import PostRepositoryProtocol, PostRepositoryDep
from .schemas import (
    PostCreateSchema,
    PostReadSchema,
    PostUpdateSchema,
    PostUpdatePartialSchema,
)

logger = logging.getLogger("post_service")


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
            logger.warning(
                f"Пользователь {user_id = } уже имеет пост с таким названием"
            )
            raise PostAlreadyExist

        post_id = await self.post_repo.create_user_post(
            user_id=user_id,
            post_data=post_data.model_dump(),
        )
        logger.info(f"Пост {post_id = } пользователя {user_id = } успешно создан!")
        return post_id

    async def get_post_by_post_id(self, user_id: int, post_id: int) -> PostReadSchema:
        post = await self.post_repo.get_user_post(user_id=user_id, id=post_id)
        if not post:
            logger.warning(PostNotFoundException.message)
            raise PostNotFoundException
        logger.info(f"Пользователь {user_id = } открыл пост {post}")
        return PostReadSchema.model_validate(post)

    async def get_posts(
        self,
        user_id: int,
        pagination: PaginationSchema,
    ) -> list[PostReadSchema]:
        posts = await self.post_repo.get_user_posts(
            user_id,
            limit=pagination.limit,
            offset=(pagination.page - 1) * pagination.limit,
        )
        logger.info(f"Пользователь {user_id = } вывел свои посты")
        return [PostReadSchema.model_validate(post) for post in posts]

    async def update_post(
        self,
        user_id: int,
        post_id: int,
        post_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> PostReadSchema:
        post = await self.post_repo.get_user_post(user_id, id=post_id)
        if not post:
            raise PostNotFoundException

        if post_data.title:
            exists_post = await self.post_repo.check_post_exists(
                user_id, title=post_data.title
            )
            if exists_post:
                logger.warning(PostAlreadyExist.message)
                raise PostAlreadyExist

        logger.info(f"Обновляем пост {post} ...")
        updated_post = await self.post_repo.update_post(
            post, update_data=post_data, partial=partial
        )
        logger.info("Пост успешно обновлен!")
        return PostReadSchema.model_validate(updated_post)

    async def delete_post(self, user_id: int, post_id: int) -> None:
        post = await self.post_repo.get_user_post(user_id, id=post_id)
        if not post:
            raise PostNotFoundException
        await self.post_repo.delete_post(post)
        logger.info(f"Пост {post.id = } успешно удален")
        return


async def get_posts_service(
    session: SessionDep,
    post_repo: PostRepositoryDep,
    user_repo: UserRepositoryDep,
) -> PostServiceProtocol:
    return PostService(session, post_repo, user_repo)


PostServiceDep = Annotated[PostServiceProtocol, Depends(get_posts_service)]
