from fastapi import Depends
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.db.session import SessionLocal
from app.models import Transaction


class TransactionOut(BaseModel):
    hash: Optional[str] = None
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    value: int
    gas: int
    gas_price: int
    block_number: int
    transaction_type: str

    class Config:
        orm_mode = True
        from_attributes = True


class TransactionStats(BaseModel):
    total_count: int
    avg_gas_price: float

    class Config:
        orm_mode = True
        from_attributes = True


class TransactionQueryParams:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 50,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        block_number: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
    ):
        self.skip = skip
        self.limit = limit
        self.from_address = from_address
        self.to_address = to_address
        self.block_number = block_number
        self.db = db
