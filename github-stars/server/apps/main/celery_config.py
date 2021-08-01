from celery import Celery
# from server.settings.components import config
from pathlib import Path
from decouple import AutoConfig

BASE_DIR = Path.cwd().parent.parent.parent.parent

config = AutoConfig(search_path=BASE_DIR.joinpath('config'))


RABBITMQ_DEFAULT_USER = config('RABBITMQ_DEFAULT_USER')
RABBITMQ_DEFAULT_PASS = config('RABBITMQ_DEFAULT_PASS')
RABBITMQ_PORT = config('RABBITMQ_PORT', cast=int, default=5672)
RABBITMQ_HOST = config('RABBITMQ_HOST')


celery_app = Celery(
    'tasks',
    broker='amqp://{login}:{password}@{host}:{port}'.format(
        login=RABBITMQ_DEFAULT_USER,
        password=RABBITMQ_DEFAULT_PASS,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
    ),
    backend='rpc://',
)

celery_app.autodiscover_tasks()
