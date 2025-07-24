from typing import Protocol, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.follows.repository import FollowsRepositoryProtocol, FollowsRepositoryDep
from core.dependencies import SessionDep
from .models import FeedType
from .repository import FeedRepositoryProtocol, FeedRepositoryDep
from .schemas import FeedReadSchema


class FeedServiceProtocol(Protocol):

    async def create_event_for_users(
        self,
        author_id: int,
        event_id: int,
        event_type: FeedType,
    ) -> None:
        pass

    async def get_user_events(self, user_id: int) -> list[FeedReadSchema]:
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
        event_id: int,
        event_type: FeedType,
    ) -> None:
        # Получаем всех подписчиков текущего пользователя
        followers_ids = await self.follows_repo.get_subs_ids(user_id=author_id)

        # Добавляем пачку событий в базу данных
        await self.feed_repo.create_event_for_users(
            author_id=author_id,
            recipients_ids=list(followers_ids),
            event_id=event_id,
            event_type=event_type,
        )
        return

    async def get_user_events(self, user_id: int) -> list[FeedReadSchema]:
        events = await self.feed_repo.get_events(user_id=user_id)
        return [FeedReadSchema.model_validate(event) for event in events]


async def get_feed_service(
    session: SessionDep,
    feed_repo: FeedRepositoryDep,
    follows_repo: FollowsRepositoryDep,
) -> FeedServiceProtocol:
    return FeedService(session, feed_repo, follows_repo)


FeedServiceDep = Annotated[FeedServiceProtocol, Depends(get_feed_service)]
