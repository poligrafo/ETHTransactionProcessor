import time
import logging
from typing import Any
from hexbytes import HexBytes
from web3.types import TxReceipt

from app.core.celery.tasks import fetch_and_save_latest_transactions
from app.core.providers.web3_provider import w3


class EthereumTransactionHandler:
    def __init__(self) -> None:
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger("EthereumTransactionHandler")
        logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def handle_transaction(self, tx_hash: HexBytes) -> None:
        """
        Handles a transaction by its hash.
        """
        try:
            self.logger.info(f"Fetching transaction receipt for {tx_hash.hex()}")
            tx_receipt: TxReceipt = w3.eth.get_transaction_receipt(tx_hash)
            if tx_receipt:
                self.logger.info(f"Processing transaction {tx_hash.hex()}")
                fetch_and_save_latest_transactions.delay(tx_receipt)
        except Exception as e:
            self.logger.error(f"Error processing transaction {tx_hash.hex()}: {e}")

    def handle_block(self, block_hash: HexBytes) -> None:
        """
        Handles a block by its hash, extracting and processing all transactions in the block.
        """
        try:
            block = w3.eth.get_block(block_hash, full_transactions=True)
            block_number = block.get('number')
            transactions = block.get('transactions', [])
            self.logger.info(
                f"Processing block {block_number} with {len(transactions)} transactions"
            )
            for tx in transactions:
                self.handle_transaction(tx.get('hash'))
        except Exception as e:
            self.logger.error(f"Error processing block {block_hash.hex()}: {e}")


class EthereumBlockListener:
    def __init__(self, transaction_handler: EthereumTransactionHandler, poll_interval: int = 2) -> None:
        self.transaction_handler = transaction_handler
        self.poll_interval = poll_interval
        self.logger = self._setup_logger()

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger("EthereumBlockListener")
        logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        return logger

    def log_loop(self, event_filter: Any) -> None:
        """
        Main loop that monitors new blocks and triggers their processing.
        """
        while True:
            self.logger.info("Checking for new blocks...")
            for event in event_filter.get_new_entries():
                self.transaction_handler.handle_block(event['blockHash'])
            time.sleep(self.poll_interval)

    def start(self) -> None:
        """
        Starts the block listener.
        """
        self.logger.info("Starting block listener...")
        block_filter = w3.eth.filter('latest')  # Create a filter to get new blocks
        self.log_loop(block_filter)  # Start the loop to process new blocks


if __name__ == "__main__":
    tx_handler = EthereumTransactionHandler()
    block_listener = EthereumBlockListener(tx_handler)
    block_listener.start()
