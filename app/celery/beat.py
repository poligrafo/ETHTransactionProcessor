from celery.schedules import crontab

from app.celery.celery_config import celery_app
from app.celery.tasks import download_yesterday_dump_task

celery_app.conf.beat_schedule = {
    'download-yesterday-dump-every-day': {
        'task': 'app.celery.tasks.download_yesterday_dump_task',
        'schedule': crontab(minute=0, hour=2),  # Daily at 02:00
    },
}

celery_app.conf.timezone = 'UTC'
