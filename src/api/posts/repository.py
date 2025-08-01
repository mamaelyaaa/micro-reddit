import logging
from typing import Protocol, Annotated, Optional, Sequence, Any

from fastapi import Depends
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.dependencies import SessionDep
from core.exceptions import BadValidationException
from .models import Post
from .schemas import PostUpdateSchema, PostUpdatePartialSchema, PostCreateSchema

logger = logging.getLogger(__name__)


class PostRepositoryProtocol(Protocol):

    async def create_user_post(
        self,
        user_id: int,
        post_data: PostCreateSchema,
    ) -> int:
        pass

    async def get_user_post(self, user_id: int, *args, **kwargs) -> Optional[Post]:
        pass

    async def get_user_posts(
        self,
        user_id: int,
        limit: int,
        offset: int,
        *args,
        **kwargs,
    ) -> Sequence[Post]:
        pass

    async def check_post_exists(self, user_id: int, title: str) -> bool:
        pass

    async def update_post(
        self,
        post: Post,
        update_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> Optional[Post]:
        pass

    async def delete_post(self, post: Post) -> None:
        pass


class PostRepository:
    """
    Репозиторий для постов авторизованного пользователя
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_post(
        self,
        user_id: int,
        post_data: PostCreateSchema,
    ) -> int:
        logger.debug('Создаем пост "%s" ...', post_data.title)
        post = Post(user_id=user_id, **post_data.model_dump())
        self.session.add(post)
        await self.session.commit()
        return post.id

    async def get_user_post(self, user_id: int, *args, **kwargs) -> Optional[Post]:
        logger.debug(f"Ищем пост пользователя #{user_id} с {kwargs} ...")
        query = select(Post).filter_by(user_id=user_id, **kwargs)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def get_user_posts(
        self,
        user_id: int,
        limit: int,
        offset: int,
        *args,
        **kwargs,
    ) -> Sequence[Post]:
        logger.debug(
            f"Ищем %d постов пользователя #%d, начиная с %d ...",
            limit,
            user_id,
            offset,
        )
        query = select(Post).filter_by(user_id=user_id, **kwargs)
        query = query.limit(limit).offset(offset)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def check_post_exists(self, user_id: int, title: str) -> bool:
        logger.debug(
            f"Проверяем существует ли пост пользователя #%d с названием %s ...",
            user_id,
            title,
        )
        query = select(Post).filter_by(user_id=user_id, title=title)
        res = await self.session.scalar(query)
        return True if res else False

    async def update_post(
        self,
        post: Post,
        update_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> Optional[Post]:
        logger.debug("Обновляем пост #%d ...", post.id)

        for key, value in update_data.model_dump(
            exclude_none=partial,
            exclude_unset=partial,
        ).items():
            if not hasattr(post, key):
                logger.error("Некорректное поле для обновления: %s", key)
                raise BadValidationException(
                    "Некорректное поле для обновления: %s", key
                )
            setattr(post, key, value)

        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def delete_post(self, post: Post) -> None:
        logger.debug("Удаляем пост #%d ...", post.id)
        stmt = delete(Post).filter_by(id=post.id, user_id=post.user_id)
        await self.session.execute(stmt)
        await self.session.commit()
        return


async def get_posts_repository(session: SessionDep) -> PostRepositoryProtocol:
    return PostRepository(session)


PostRepositoryDep = Annotated[PostRepositoryProtocol, Depends(get_posts_repository)]
