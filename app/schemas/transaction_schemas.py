from pydantic import BaseModel


class TransactionBase(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: float
    gas: int
    gas_price: float
    block_number: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
