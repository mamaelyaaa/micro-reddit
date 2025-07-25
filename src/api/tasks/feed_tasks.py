import logging
from typing import Annotated

from taskiq import TaskiqDepends

from api.feeds.models import FeedType
from api.feeds.service import FeedServiceProtocol, get_feed_service
from core.broker import broker

logger = logging.getLogger("feed_tasks")


FeedServiceTaskiqDep = Annotated[FeedServiceProtocol, TaskiqDepends(get_feed_service)]


@broker.task(task_name="create_event_for_users")
async def create_event_for_users(
    feed_service: FeedServiceTaskiqDep,
    author_id: int,
    event_id: int,
    event_type: FeedType,
) -> None:
    logger.info(
        f"Отправляем задачу на обновление событий {author_id = }, {event_id = }, event_type = {event_type.upper()}"
    )
    await feed_service.create_event_for_users(author_id, event_id, event_type)
    logger.info(f"Задача create_event_for_users выполнена")
    return
