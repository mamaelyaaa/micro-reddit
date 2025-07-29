import logging
from typing import Annotated

from taskiq import TaskiqDepends

from api.feeds.service import FeedServiceProtocol, get_feed_service
from core.broker import broker

logger = logging.getLogger(__name__)


FeedServiceTaskiqDep = Annotated[FeedServiceProtocol, TaskiqDepends(get_feed_service)]


@broker.task(task_name="create_event_for_users")
async def create_event_for_users(
    feed_service: FeedServiceTaskiqDep,
    author_id: int,
    post_id: int,
) -> None:
    logger.info(f"Отправляем задачу на обновление событий {author_id = }, {post_id = }")
    await feed_service.create_event_for_users(author_id, post_id)
    logger.info(
        "Подписчики пользователя #%d увидят его новый пост #%d!", author_id, post_id
    )
    return
