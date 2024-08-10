from pydantic_settings import BaseSettings
from typing import ClassVar, Dict, Any
from celery.schedules import crontab


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    INFURA_API_KEY: str

    CELERY_BROKER_URL: str = "redis://redis:6388/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6388/0"

    CELERY_BEAT_SCHEDULE: ClassVar[Dict[str, Dict[str, Any]]] = {
        'download_yesterday_dump_every_day': {
            'task': 'app.celery.tasks.download_yesterday_dump_task',
            'schedule': crontab(minute='55', hour='13'),  # Daily at 04:00 UTC (+3 MSK)
        },
    }

    CELERY_TIMEZONE: str = 'UTC'
    CELERY_ENABLE_UTC: bool = True
    BROKER_CONNECTION_RETRY_ON_STARTUP: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
