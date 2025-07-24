import taskiq_fastapi
from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(
    url="amqp://guest:guest@localhost:5672/",
)

taskiq_fastapi.init(broker, app_or_path="main:app")