from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    tx_hash: str
    block_number: int
    from_address: str
    to_address: str
    value: float
    gas_used: int
    gas_price_wei: float


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
