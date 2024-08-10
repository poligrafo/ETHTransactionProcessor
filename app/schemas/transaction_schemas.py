# from pydantic import BaseModel
#
#
# class TransactionBase(BaseModel):
#     hash: str
#     from_address: str
#     to_address: str
#     value: float
#     gas: int
#     gas_price: float
#     block_number: int
#
#
# class TransactionCreate(TransactionBase):
#     pass
#
#
# class Transaction(TransactionBase):
#     id: int
#
#     class Config:
#         orm_mode = True


from pydantic import BaseModel
from typing import Optional


class TransactionOut(BaseModel):
    hash: str
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
