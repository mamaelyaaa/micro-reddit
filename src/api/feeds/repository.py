import logging
from typing import Protocol, Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.dependencies import SessionDep
from .models import FeedType, UserFeed

logger = logging.getLogger(__name__)


class FeedRepositoryProtocol(Protocol):

    async def create_event_for_users(
        self,
        author_id: int,
        recipients_ids: list[int],
        event_id: int,
        event_type: FeedType,
    ) -> None:
        """Создает новость для пользователей (подписчиков)"""
        pass

    async def get_count_events(self, user_id: int) -> int:
        """
        Получает количество всех новостей для пользователя
        Для полноценного вывода с пагинацией
        """
        pass

    async def get_events_with_authors(self, user_id: int, offset: int, limit: int) -> Sequence[UserFeed]:
        """Получаем новость для пользователя с его автором"""
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

    async def get_count_events(self, user_id: int) -> int:
        logger.debug(
            f"Получаем общее количество новостей для пользователя {user_id = } ..."
        )
        query = select(func.count(UserFeed.id).filter(UserFeed.recipient_id == user_id))
        res = await self.session.execute(query)
        return res.scalar_one()

    async def get_events_with_authors(self, user_id: int, offset: int, limit: int) -> Sequence[UserFeed]:
        logger.debug(f"Получаем новости пользователя {user_id = } с их авторами  ...")
        query = (
            select(UserFeed)
            .options(joinedload(UserFeed.author))
            .filter_by(recipient_id=user_id)
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(query)
        return res.scalars().all()


async def get_feed_repository(session: SessionDep) -> FeedRepositoryProtocol:
    return FeedRepository(session)


FeedRepositoryDep = Annotated[FeedRepositoryProtocol, Depends(get_feed_repository)]
