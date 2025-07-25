import logging

from api.feeds.models import FeedType
from api.feeds.service import FeedServiceDep, FeedServiceProtocol
from core.broker import broker

logger = logging.getLogger("tasks")


@broker.task(task_name="create_event_for_users")
async def create_event_for_users(
    feed_service: FeedServiceProtocol,
    author_id: int,
    event_id: int,
    event_type: FeedType,
) -> None:
    logger.info(
        f"Отправляем задачу на обновление событий {author_id = }, {event_id = }, event_type = {event_type.upper()}"
    )
    await feed_service.create_event_for_users(author_id, event_id, event_type)
    return
