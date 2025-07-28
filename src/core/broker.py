import logging

import taskiq_fastapi
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

from core import settings

broker = AioPikaBroker(url=settings.broker.AMQP_DSN)

taskiq_fastapi.init(broker, app_or_path="main:app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(level=settings.log.level, format=settings.log.worker_format)
