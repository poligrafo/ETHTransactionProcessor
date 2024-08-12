import time
import logging

from app.celery.tasks import fetch_and_save_latest_transactions
from app.providers.web3_provider import w3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def handle_transaction(tx_hash):
    """
    Handles a transaction by its hash.
    """
    try:
        logger.info(f"Fetching transaction receipt for {tx_hash.hex()}")
        tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
        if tx_receipt:
            logger.info(f"Processing transaction {tx_hash.hex()}")
            fetch_and_save_latest_transactions.delay(tx_receipt)
    except Exception as e:
        logger.error(f"Error processing transaction {tx_hash.hex()}: {e}")


def handle_block(block_hash):
    """
    Handles a block by its hash, extracting and processing all transactions in the block.
    """
    try:
        block = w3.eth.get_block(block_hash, full_transactions=True)
        logger.info(f"Processing block {block.number} with {len(block.transactions)} transactions")
        for tx in block.transactions:
            handle_transaction(tx.hash)
    except Exception as e:
        logger.error(f"Error processing block {block_hash.hex()}: {e}")


def log_loop(event_filter, poll_interval):
    """
    Main loop that monitors new blocks and triggers their processing.
    """
    while True:
        logger.info("Checking for new blocks...")
        for event in event_filter.get_new_entries():
            handle_block(event['blockHash'])
        time.sleep(poll_interval)


def start_block_listener():
    """
    Starts the block listener.
    """
    logger.info("Starting block listener...")
    block_filter = w3.eth.filter('latest')  # Create a filter to get new blocks
    log_loop(block_filter, 2)  # Start the loop to process new blocks


if __name__ == "__main__":
    start_block_listener()
