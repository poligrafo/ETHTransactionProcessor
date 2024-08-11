import asyncio
import logging

from app.celery.celery_config import celery_app
from app.services.blockchair_services import download_ethereum_transactions_dump, process_and_save_transactions
from app.services.ethereum_servises import fetch_and_save_latest_transactions

logger = logging.getLogger(__name__)


@celery_app.task
def fetch_and_save_transactions_task():
    fetch_and_save_latest_transactions()


@celery_app.task
def download_yesterday_dump_task():
    logger.info("Starting task to download yesterday's Ethereum transactions dump.")
    try:
        file_path = download_ethereum_transactions_dump()
        logger.info(f"File downloaded successfully: {file_path}")
        asyncio.run(process_and_save_transactions(file_path))
        logger.info("Transactions processed and saved successfully.")
    except Exception as e:
        logger.error(f"Error in downloading or processing the file: {str(e)}")
