from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.session import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    tx_hash = Column(String, unique=True, index=True, nullable=False)
    block_number = Column(Integer, index=True)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    value = Column(Float)
    gas_used = Column(Integer)
    gas_price_wei = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
