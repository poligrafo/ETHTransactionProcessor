import os
from datetime import datetime, timedelta
import requests


def download_ethereum_transactions_dump():
    # Calculating the date yesterday
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
        print(f"The {local_filename} file has been uploaded successfully")
    else:
        print(f"The {local_filename} file already exists")

    return local_filename
