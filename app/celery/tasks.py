import asyncio
import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from web3.types import TxReceipt

from app.celery.celery_config import celery_app
from app.db.session import SessionLocal
from app.models import Transaction
from app.providers.web3_provider import w3
from app.services.blockchair_services import download_ethereum_transactions_dump, process_and_save_transactions

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@celery_app.task
async def fetch_and_save_latest_transactions(tx_receipt):
    """
    Fetches and saves the latest transactions to the database.
    """
    try:
        async with SessionLocal() as session:
            async with session.begin():
                block_time = datetime.utcfromtimestamp(w3.eth.get_block(tx_receipt['blockNumber'])['timestamp'])

                transaction = Transaction(
                    hash=tx_receipt['transactionHash'].hex(),
                    from_address=tx_receipt['from'],
                    to_address=tx_receipt.get('to'),
                    value=tx_receipt.get('value', 0),
                    gas=tx_receipt['gasUsed'],
                    gas_price=tx_receipt['effectiveGasPrice'],
                    fee=tx_receipt['gasUsed'] * tx_receipt['effectiveGasPrice'],
                    nonce=tx_receipt['transactionIndex'],
                    block_number=tx_receipt['blockNumber'],
                    time=block_time,
                    input_hex=tx_receipt.get('input', ''),
                    transaction_type=str(tx_receipt.get('type', 'normal')),
                )
                session.add(transaction)
                await session.commit()

        logger.info(f"Transaction {tx_receipt['transactionHash'].hex()} processed and saved successfully.")
    except Exception as e:
        logger.error(f"Error processing transaction {tx_receipt['transactionHash'].hex()}: {e}")


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
