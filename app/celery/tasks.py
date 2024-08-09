from app.celery.celery_config import celery_app
from app.services.blockchair_services import download_ethereum_transactions_dump
from app.services.ethereum_servises import fetch_and_save_latest_transactions


@celery_app.task
def fetch_and_save_transactions_task():
    fetch_and_save_latest_transactions()


@celery_app.task
def download_yesterday_dump_task():
    download_ethereum_transactions_dump()
