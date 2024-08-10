import os
import gzip
import pandas as pd
from datetime import datetime, timedelta
import requests
import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.transaction_models import Transaction

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


def process_and_save_transactions(file_path):
    logger.info(f"Processing the file {file_path}")
    try:
        with gzip.open(file_path, 'rt') as f:
            df = pd.read_csv(f, delimiter='\t')

        transactions = []
        for _, row in df.iterrows():
            transaction = Transaction(
                hash=row['hash'],
                time=row['time'],
                failed=bool(row['failed']),
                type=row['type'],
                from_address=row['sender'],
                to_address=row['recipient'],
                call_count=int(row['call_count']),
                value=row['value'],
                value_usd=row['value_usd'],
                internal_value=row['internal_value'],
                internal_value_usd=row['internal_value_usd'],
                fee=row['fee'],
                fee_usd=row['fee_usd'],
                gas_used=int(row['gas_used']),
                gas_limit=int(row['gas_limit']),
                gas_price=row['gas_price'],
                input_hex=row['input_hex'],
                nonce=int(row['nonce']) if pd.notnull(row['nonce']) else None,
                v=row['v'],
                r=row['r'],
                s=row['s'],
                block_number=int(row['block_id']) if pd.notnull(row['block_id']) else None,
            )
            transactions.append(transaction)

        logger.info(f"Inserting {len(transactions)} transactions into the database.")
        with SessionLocal() as session:
            session.bulk_save_objects(transactions)
            session.commit()

        logger.info("Transactions have been successfully saved to the database.")
        os.remove(file_path)
        logger.info(f"File {file_path} deleted after processing.")
    except Exception as e:
        logger.error(f"Error processing the file {file_path}: {str(e)}")
