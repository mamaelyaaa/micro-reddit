from typing import Protocol, Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.dependencies import SessionDep
from .repository import PostRepositoryProtocol, PostRepositoryDep
from .schemas import PostCreateSchema, PostReadSchema


class PostServiceProtocol(Protocol):

    async def create_post(self, user_id: int, post_data: PostCreateSchema) -> int:
        pass

    async def get_post_by_title(self, user_id: int, title: str) -> PostReadSchema:
        pass

    async def get_posts(self, user_id: int) -> list[PostReadSchema]:
        pass

    async def update_post(self, user_id: int, post_id: int, post_data):
        pass

    # async def get_user_post_by_title(self, user_id: int, title: str) -> PostReadSchema:
    #     pass
    #
    # async def get_posts(self, user_id: int) -> list[PostReadSchema]:
    #     pass


class PostService:

    def __init__(self, session: AsyncSession, post_repo: PostRepositoryProtocol):
        self.session = session
        self.post_repo = post_repo

    async def create_post(self, user_id: int, post_data: PostCreateSchema) -> int:
        post_id = await self.post_repo.create_user_post(
            self.session, post_data=post_data.model_dump(), user_id=user_id
        )
        return post_id

    async def get_post_by_title(self, user_id: int, title: str) -> PostReadSchema:
        pass

    async def get_posts(self, user_id: int) -> list[PostReadSchema]:
        posts = await self.post_repo.get_user_posts(self.session, user_id=user_id)
        return [PostReadSchema.model_validate(post) for post in posts]

    async def update_post(self, user_id: int, post_id: int, post_data):
        pass


async def get_posts_service(
    session: SessionDep, post_repo: PostRepositoryDep
) -> PostServiceProtocol:
    return PostService(session, post_repo)


PostRepositoryDep = Annotated[PostServiceProtocol, Depends(get_posts_service)]


class AdminPostServiceProtocol(PostServiceProtocol, Protocol):
    pass
