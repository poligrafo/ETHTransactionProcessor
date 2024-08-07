from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    tx_hash: str
    block_number: int
    from_address: str
    to_address: str
    value: float
    gas: int
    gas_price: float


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
