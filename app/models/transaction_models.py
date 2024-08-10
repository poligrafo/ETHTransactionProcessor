from sqlalchemy import Column, Integer, String, Numeric, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, index=True)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    value = Column(Numeric)
    gas = Column(Integer)
    gas_price = Column(Numeric)
    fee = Column(Numeric)  # Комиссия за транзакцию (gas * gas_price)
    nonce = Column(Integer)  # Nonce транзакции
    block_number = Column(Integer, index=True)
    time = Column(DateTime)  # Время включения транзакции в блок
    input_hex = Column(String)  # Входные данные транзакции в hex-формате

    __table_args__ = (
        Index('ix_transactions_hash', 'hash'),
        Index('ix_transactions_from_address', 'from_address'),
        Index('ix_transactions_to_address', 'to_address'),
        Index('ix_transactions_block_number', 'block_number'),
    )
