import requests
import os
import gzip
import pandas as pd
import logging

from app.db.session import SessionLocal
from app.models.transaction_models import Transaction
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def download_ethereum_transactions_dump():
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime('%Y%m%d')

    url = f'https://gz.blockchair.com/ethereum/transactions/blockchair_ethereum_transactions_{date_str}.tsv.gz'
    local_filename = f'/app/data/blockchair_ethereum_transactions_{date_str}.tsv.gz'

    if not os.path.exists(local_filename):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        logger.info(f"The {local_filename} file has been downloaded successfully")
    else:
        logger.info(f"The {local_filename} file already exists")

    return local_filename


async def process_and_save_transactions(file_path: str):
    logger.info(f"Processing the file {file_path}")
    try:
        logger.info("Opening the gzip file...")
        with gzip.open(file_path, 'rt') as f:
            logger.info("Reading the CSV content into a DataFrame...")
            df = pd.read_csv(f, delimiter='\t')
            logger.info(f"DataFrame loaded successfully with {len(df)} rows.")

        transactions = []
        logger.info("Iterating over the DataFrame rows...")
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

        logger.info(f"Inserting {len(transactions)} transactions into the database.")

        async with SessionLocal() as session:
            async with session.begin():
                session.add_all(transactions)
                await session.commit()

        logger.info("Transactions have been successfully saved to the database.")
        os.remove(file_path)
        logger.info(f"File {file_path} deleted after processing.")
    except Exception as e:
        logger.error(f"Error processing the file {file_path}: {str(e)}")
