import logging
from typing import Protocol, Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import SessionDep
from .models import FeedType, UserFeed

logger = logging.getLogger("feeds_repo")


class FeedRepositoryProtocol(Protocol):

    async def create_event_for_users(
        self,
        author_id: int,
        recipients_ids: list[int],
        event_id: int,
        event_type: FeedType,
    ) -> None:
        pass

    async def get_events(self, user_id: int) -> Sequence[UserFeed]:
        pass


class FeedRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_event_for_users(
        self,
        author_id: int,
        recipients_ids: list[int],
        event_id: int,
        event_type: FeedType,
    ) -> None:
        logger.debug(f"Создаем события для пользователей {recipients_ids = }...")

        for recipient_id in recipients_ids:
            event = UserFeed(
                author_id=author_id,
                recipient_id=recipient_id,
                event_id=event_id,
                event_type=event_type,
            )
            self.session.add(event)

        await self.session.commit()
        return

    async def get_events(self, user_id: int) -> Sequence[UserFeed]:
        logger.debug(f"Пользователь {user_id = } получает новости...")
        query = select(UserFeed).filter_by(recipient_id=user_id)
        res = await self.session.execute(query)
        return res.scalars().all()


async def get_feed_repository(session: SessionDep) -> FeedRepositoryProtocol:
    return FeedRepository(session)


FeedRepositoryDep = Annotated[FeedRepositoryProtocol, Depends(get_feed_repository)]
