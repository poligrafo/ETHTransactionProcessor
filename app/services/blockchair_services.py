import requests
import os
import gzip
import pandas as pd
import logging
from typing import List

from app.db.session import SessionLocal
from app.models.transaction_models import Transaction
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EthereumTransactionsDownloader:
    def __init__(self) -> None:
        self.yesterday = datetime.now() - timedelta(days=1)
        self.date_str = self.yesterday.strftime('%Y%m%d')
        self.url = (
            f'https://gz.blockchair.com/ethereum/transactions/'
            f'blockchair_ethereum_transactions_{self.date_str}.tsv.gz'
        )
        self.local_filename = f'/app/data/blockchair_ethereum_transactions_{self.date_str}.tsv.gz'

    def file_exists(self) -> bool:
        return os.path.exists(self.local_filename)

    def download(self) -> str:
        if not self.file_exists():
            with requests.get(self.url, stream=True) as r:
                r.raise_for_status()
                with open(self.local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            logger.info(f"The {self.local_filename} file has been downloaded successfully")
        else:
            logger.info(f"The {self.local_filename} file already exists")

        return self.local_filename


class EthereumTransactionsProcessor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_data(self) -> pd.DataFrame:
        logger.info(f"Processing the file {self.file_path}")
        logger.info("Opening the gzip file...")
        with gzip.open(self.file_path, 'rt') as f:
            logger.info("Reading the CSV content into a DataFrame...")
            df = pd.read_csv(f, delimiter='\t')
            logger.info(f"DataFrame loaded successfully with {len(df)} rows.")
        return df

    @staticmethod
    def parse_transactions(df: pd.DataFrame) -> List[Transaction]:
        logger.info("Iterating over the DataFrame rows...")
        transactions: List[Transaction] = []
        for _, row in df.iterrows():
            transaction = Transaction(
                hash=row['hash'] if pd.notnull(row['hash']) else None,
                from_address=row['sender'] if pd.notnull(row['sender']) else None,
                to_address=row['recipient'] if pd.notnull(row['recipient']) else None,
                value=row['value'] if pd.notnull(row['value']) else None,
                gas=int(row['gas_used']) if pd.notnull(row['gas_used']) else None,
                gas_price=row['gas_price'] if pd.notnull(row['gas_price']) else None,
                block_number=int(row['block_id']) if pd.notnull(row['block_id']) else None,
                transaction_type=row['type'] if pd.notnull(row['type']) else None,
            )
            transactions.append(transaction)
        return transactions

    @staticmethod
    async def save_transactions(transactions: List[Transaction]) -> None:
        logger.info(f"Inserting {len(transactions)} transactions into the database.")
        async with SessionLocal() as session:
            async with session.begin():
                session.add_all(transactions)
                await session.commit()

    def cleanup(self) -> None:
        os.remove(self.file_path)
        logger.info(f"File {self.file_path} deleted after processing.")

    async def process(self) -> None:
        try:
            df = self.load_data()
            transactions = self.parse_transactions(df)
            await self.save_transactions(transactions)
            self.cleanup()
        except Exception as e:
            logger.error(f"Error processing the file {self.file_path}: {str(e)}")
