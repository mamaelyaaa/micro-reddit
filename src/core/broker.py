import taskiq_fastapi
from taskiq_aio_pika import AioPikaBroker

from core import settings

broker = AioPikaBroker(url=settings.broker.AMQP_DSN)

taskiq_fastapi.init(broker, app_or_path="main:app")

