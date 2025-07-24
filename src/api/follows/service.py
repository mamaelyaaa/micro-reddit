from typing import Protocol, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.follows.exceptions import FollowAlreadyExists, SelfFollowError, FollowNotFound
from api.follows.repository import FollowsRepositoryProtocol, FollowsRepositoryDep
from core.dependencies import SessionDep


class FollowsServiceProtocol(Protocol):

    async def subscribe_user(self, cur_user_id: int, target_id: int) -> None:
        pass

    async def unsubscribe_user(self, cur_user_id: int, target_id: int) -> None:
        pass


class FollowsService:

    def __init__(self, session: AsyncSession, follows_repo: FollowsRepositoryProtocol):
        self.session = session
        self.follows_repo = follows_repo

    async def subscribe_user(self, cur_user_id: int, target_id: int) -> None:
        if cur_user_id == target_id:
            raise SelfFollowError

        exists_follow = await self.follows_repo.get_subscription(
            follower_id=cur_user_id, followee_id=target_id
        )
        if exists_follow:
            raise FollowAlreadyExists

        await self.follows_repo.create_subscription(
            follower_id=cur_user_id, followee_id=target_id
        )
        return

    async def unsubscribe_user(self, cur_user_id: int, target_id: int) -> None:
        follow = await self.follows_repo.get_subscription(
            follower_id=cur_user_id, followee_id=target_id
        )
        if not follow:
            raise FollowNotFound

        await self.follows_repo.delete_subscription(follow)
        return


async def get_follows_service(
    session: SessionDep,
    follows_repo: FollowsRepositoryDep,
) -> FollowsServiceProtocol:
    return FollowsService(session, follows_repo)


FollowsServiceDep = Annotated[FollowsServiceProtocol, Depends(get_follows_service)]
