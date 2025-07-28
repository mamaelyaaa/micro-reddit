import logging
from typing import Protocol, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.follows.repository import FollowsRepositoryProtocol, FollowsRepositoryDep
from core.dependencies import SessionDep
from schemas import SearchResponseSchema, PaginationSchema
from .repository import FeedRepositoryProtocol, FeedRepositoryDep
from .schemas import FeedDetailSchema

logger = logging.getLogger(__name__)


class FeedServiceProtocol(Protocol):

    async def create_event_for_users(
        self,
        author_id: int,
        post_id: int,
    ) -> None:
        pass

    async def get_user_events(
        self,
        user_id: int,
        pagination: PaginationSchema,
    ) -> SearchResponseSchema[FeedDetailSchema]:
        """Получаем автора поста, сам пост, тип поста, пагинацию и общее количество"""
        pass


class FeedService:

    def __init__(
        self,
        session: AsyncSession,
        feed_repo: FeedRepositoryProtocol,
        follows_repo: FollowsRepositoryProtocol,
    ):
        self.session = session
        self.feed_repo = feed_repo
        self.follows_repo = follows_repo

    async def create_event_for_users(
        self,
        author_id: int,
        post_id: int,
    ) -> None:
        # Получаем всех подписчиков текущего пользователя
        followers_ids = await self.follows_repo.get_subs_ids(user_id=author_id)

        if not followers_ids:
            logger.warning("События рассылать некому")
            return

        # Добавляем пачку событий в базу данных
        await self.feed_repo.create_event_for_users(
            author_id=author_id,
            recipients_ids=list(followers_ids),
            post_id=post_id,
        )
        return

    async def get_user_events(
        self,
        user_id: int,
        pagination: PaginationSchema,
    ) -> SearchResponseSchema[FeedDetailSchema]:
        # Собираем количество всех новостей
        total_events = await self.feed_repo.get_count_events(user_id)

        # Подтягиваем автора новости и саму новость
        events_with_authors = await self.feed_repo.get_full_events_with_authors(
            user_id=user_id,
            limit=pagination.limit,
            offset=(pagination.page - 1) * pagination.limit,
        )

        return SearchResponseSchema(
            detail=[
                FeedDetailSchema.model_validate(event) for event in events_with_authors
            ],
            total_found=total_events,
            pagination=pagination,
        )


async def get_feed_service(
    session: SessionDep,
    feed_repo: FeedRepositoryDep,
    follows_repo: FollowsRepositoryDep,
) -> FeedServiceProtocol:
    return FeedService(session, feed_repo, follows_repo)


FeedServiceDep = Annotated[FeedServiceProtocol, Depends(get_feed_service)]
