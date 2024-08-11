from pydantic import BaseModel
from typing import Optional


class TransactionOut(BaseModel):
    hash: Optional[str] = None
    from_address: str
    to_address: Optional[str] = None
    value: int
    gas: int
    gas_price: int
    block_number: int

    class Config:
        orm_mode = True


class TransactionStats(BaseModel):
    total_count: int
    avg_gas_price: float
