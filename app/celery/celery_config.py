from celery import Celery

from app.core.settings import settings
from app.core.logging import setup_logging

setup_logging()

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=settings.CELERY_ENABLE_UTC,
    broker_connection_retry_on_startup=settings.BROKER_CONNECTION_RETRY_ON_STARTUP,
)

celery_app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE

