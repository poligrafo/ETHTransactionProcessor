import pytest
from web3 import Web3
from app.core.celery.tasks import fetch_and_save_latest_transactions
from app.db.session import SessionLocal
from app.models.transaction_models import Transaction
from sqlalchemy.future import select
from app.core.settings import settings
from hexbytes import HexBytes


@pytest.fixture(scope='module')
def infura_connection():
    infura_url = f"https://mainnet.infura.io/v3/{settings.INFURA_API_KEY}"
    w3 = Web3(Web3.HTTPProvider(infura_url))
    assert w3.is_connected(), "Failed to connect to Infura"
    return w3


@pytest.mark.asyncio
async def test_fetch_and_save_latest_transactions(infura_connection):
    tx_hash = HexBytes("2f4228659dee1416b88e984be9b8a19fad8fa6ee8c9f7cdc0c80c7869da8bf8a")
    tx_receipt = infura_connection.eth.get_transaction_receipt(tx_hash)

    print(f"Received transaction receipt: {tx_receipt}")

    async with SessionLocal() as db_session:
        async with db_session.begin():
            await fetch_and_save_latest_transactions(tx_receipt)
            result = await db_session.execute(
                select(Transaction).filter_by(hash=tx_receipt['transactionHash'].hex())
            )
            saved_transaction = result.scalars().first()

    assert saved_transaction is not None, "Transaction was not saved to the database"
