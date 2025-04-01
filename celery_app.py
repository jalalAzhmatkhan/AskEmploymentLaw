import os

from celery import Celery

from core.configs import settings

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
celery_application = Celery(
    'celery_app',
    broker=f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@"
           f"{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}"
)

celery_application.conf.result_backend = "rpc://"
celery_application.conf.task_routes = {
    "document_management_service.get_dense_vector_from_text": "main-queue"
}
celery_application.conf.task_serializer = 'json'
