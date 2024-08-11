from celery import Celery
from celery.schedules import crontab
import os


class CeleryConfig:
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6388/0')

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TIMEZONE = 'UTC'
    CELERY_ENABLE_UTC = True
    BROKER_CONNECTION_RETRY_ON_STARTUP = True
    TASK_TRACK_STARTED = True

    CELERY_BEAT_SCHEDULE = {
        'download_yesterday_dump_every_day': {
            'task': 'app.celery.tasks.download_yesterday_dump_task',
            'schedule': crontab(minute=55, hour=17),  # Daily at 04:00 UTC (+3 MSK)
        },
    }


def create_celery_app():
    celery_app = Celery(
        'worker',
        broker=CeleryConfig.CELERY_BROKER_URL,
        backend=CeleryConfig.CELERY_RESULT_BACKEND
    )

    celery_app.conf.update(
        task_track_started=CeleryConfig.TASK_TRACK_STARTED,
        timezone=CeleryConfig.CELERY_TIMEZONE,
        enable_utc=CeleryConfig.CELERY_ENABLE_UTC,
        broker_connection_retry_on_startup=CeleryConfig.BROKER_CONNECTION_RETRY_ON_STARTUP,
        beat_schedule=CeleryConfig.CELERY_BEAT_SCHEDULE,
    )

    celery_app.autodiscover_tasks(['app.celery.tasks'])

    return celery_app


celery_app = create_celery_app()
