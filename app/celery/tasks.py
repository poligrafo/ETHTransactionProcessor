from app.celery.celery_config import celery_app
from app.services.ethereum_servises import fetch_and_save_latest_transactions


@celery_app.task
def fetch_and_save_transactions_task():
    fetch_and_save_latest_transactions()
