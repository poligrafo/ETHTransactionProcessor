from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional

from app.models.transaction_models import Transaction


async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 50, from_address: Optional[str] = None,
                           to_address: Optional[str] = None, block_number: Optional[int] = None):
    query = select(Transaction).offset(skip).limit(limit)

    if from_address:
        query = query.filter(Transaction.from_address == from_address)
    if to_address:
        query = query.filter(Transaction.to_address == to_address)
    if block_number:
        query = query.filter(Transaction.block_number == block_number)

    result = await db.execute(query)
    return result.scalars().all()


async def get_transaction_by_hash(db: AsyncSession, tx_hash: str) -> Optional[Transaction]:
    result = await db.execute(select(Transaction).filter(Transaction.hash == tx_hash))
    return result.scalar_one_or_none()


async def get_transaction_stats(db: AsyncSession):
    total_count = await db.execute(select(func.count(Transaction.id)))
    avg_gas_price = await db.execute(select(func.avg(Transaction.gas_price)))
    return {
        "total_count": total_count.scalar(),
        "avg_gas_price": avg_gas_price.scalar()
    }
