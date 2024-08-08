from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.crud.base import CRUDBase
from sqlalchemy.future import select

from app.models.transaction_models import Transaction
from app.schemas.transaction_schemas import TransactionCreate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate]):
    async def get_by_tx_hash(self, db: AsyncSession, tx_hash: str) -> Optional[Transaction]:
        result = await db.execute(select(self.model).filter(self.model.tx_hash == tx_hash))
        return result.scalars().first()


transaction = CRUDTransaction(Transaction)
