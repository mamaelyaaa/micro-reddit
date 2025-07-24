import logging
from typing import Protocol, Annotated, Optional

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.follows.models import Follow
from core.dependencies import SessionDep

logger = logging.getLogger("follows_repo")


class FollowsRepositoryProtocol(Protocol):

    async def create_subscription(self, follower_id: int, followee_id: int) -> None:
        pass

    async def delete_subscription(self, follow: Follow) -> None:
        pass

    async def get_subscription(
        self, follower_id: int, followee_id: int
    ) -> Optional[Follow]:
        pass


class FollowsRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_subscription(self, follower_id: int, followee_id: int) -> None:
        logger.debug(
            f"Пользователь {follower_id = } подписывается на {followee_id = } ..."
        )
        follow = Follow(follower_id=follower_id, followee_id=followee_id)
        self.session.add(follow)
        await self.session.commit()
        return

    async def delete_subscription(self, follow: Follow) -> None:
        logger.debug(
            f"Пользователь {follow.follower_id = } отписывается от {follow.followee_id = } ..."
        )
        stmt = delete(Follow).filter_by(
            follower_id=follow.follower_id,
            followee_id=follow.followee_id,
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return

    async def get_subscription(
        self, follower_id: int, followee_id: int
    ) -> Optional[Follow]:
        logger.debug(
            f"Ищем подписку пользователя {follower_id = } на {followee_id = } ..."
        )
        query = select(Follow).filter_by(
            follower_id=follower_id, followee_id=followee_id
        )
        follow = await self.session.scalar(query)
        return follow


async def get_follows_repository(session: SessionDep) -> FollowsRepositoryProtocol:
    return FollowsRepository(session)


FollowsRepositoryDep = Annotated[
    FollowsRepositoryProtocol, Depends(get_follows_repository)
]
