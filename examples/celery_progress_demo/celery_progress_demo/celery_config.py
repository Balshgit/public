from celery import Celery


github_celery_app = Celery(
    'tasks',
    broker='amqp://{login}:{password}@{host}:{port}'.format(
        login='rabbit_admin',
        password='mypass',
        host='localhost',
        port='5672',),
    backend='rpc://',
)

github_celery_app.autodiscover_tasks()
