from typing import Protocol, Annotated, Optional, Sequence, Literal

from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from core.dependencies import SessionDep
from core.exceptions import BadRequestException, NotFoundException
from .models import Post
from .schemas import PostCreateSchema, PostUpdateSchema, PostUpdatePartialSchema


class PostRepositoryProtocol(Protocol):

    async def create_user_post(self, user_id: int, post_data: dict) -> int:
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
        user_id: int,
        post_id: int,
        update_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> Optional[Post]:
        pass


class PostRepository:
    """Репозиторий постов конкретного пользователя"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user_post(self, user_id: int, post_data: dict) -> int:
        post = Post(user_id=user_id, **post_data)
        self.session.add(post)
        await self.session.commit()
        return post.id

    async def get_user_post(self, user_id: int, *args, **kwargs) -> Optional[Post]:
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
        query = select(Post).filter_by(user_id=user_id, **kwargs)
        query = query.limit(limit).offset(offset)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def check_post_exists(self, user_id: int, title: str) -> bool:
        query = select(Post).filter_by(user_id=user_id, title=title)
        res = await self.session.scalar(query)
        return True if res else False

    async def update_post(
        self,
        user_id: int,
        post_id: int,
        update_data: PostUpdateSchema | PostUpdatePartialSchema,
        partial: bool,
    ) -> Optional[Post]:
        post = await self.get_user_post(user_id=user_id, id=post_id)
        if not post:
            raise NotFoundException("Пост не найден")

        for key, value in update_data.model_dump(
            exclude_none=partial, exclude_unset=partial
        ).items():
            if not hasattr(post, key):
                raise
            setattr(post, key, value)

        await self.session.commit()
        await self.session.refresh(post)
        return post


async def get_posts_repository(session: SessionDep) -> PostRepositoryProtocol:
    return PostRepository(session)


PostRepositoryDep = Annotated[PostRepositoryProtocol, Depends(get_posts_repository)]
