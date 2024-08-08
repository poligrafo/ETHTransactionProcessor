from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.models import Transaction
from app.services.infura_services import InfuraService

infura_service = InfuraService()


async def save_transactions(transactions):
    async with SessionLocal() as session:
        async with session.begin():
            for tx in transactions:
                transaction = Transaction(
                    hash=tx['hash'],
                    from_address=tx['from'],
                    to_address=tx['to'],
                    value=tx['value'],
                    gas=tx['gas'],
                    gas_price=tx['gasPrice'],
                    block_number=tx['blockNumber']
                )
                session.add(transaction)
        await session.commit()


async def fetch_and_save_latest_transactions():
    block_number = infura_service.get_latest_block_number()
    block = infura_service.get_block_by_number(block_number)
    transactions = block['transactions']
    await save_transactions(transactions)
