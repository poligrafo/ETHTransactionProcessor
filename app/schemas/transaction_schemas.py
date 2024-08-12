from pydantic import BaseModel
from typing import Optional


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
