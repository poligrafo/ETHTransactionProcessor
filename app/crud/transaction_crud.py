# from sqlalchemy.ext.asyncio import AsyncSession
# from typing import Optional
# from app.crud.base import CRUDBase
# from sqlalchemy.future import select
#
# from app.models.transaction_models import Transaction
# from app.schemas.transaction_schemas import TransactionCreate
#
#
# class CRUDTransaction(CRUDBase[Transaction, TransactionCreate]):
#     async def get_by_tx_hash(self, db: AsyncSession, tx_hash: str) -> Optional[Transaction]:
#         result = await db.execute(select(self.model).filter(self.model.tx_hash == tx_hash))
#         return result.scalars().first()
#
#
# transaction = CRUDTransaction(Transaction)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models.transaction_models import Transaction
from typing import List, Optional


async def get_transactions(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Transaction]:
    result = await db.execute(select(Transaction).offset(skip).limit(limit))
    return list(result.scalars().all())


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


