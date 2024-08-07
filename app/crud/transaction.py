from sqlalchemy.orm import Session
from typing import Optional

from app.crud.base import CRUDBase
from app.models.transaction_models import Transaction
from app.schemas.transaction_schemas import TransactionCreate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate]):
    def get_by_tx_hash(self, db: Session, tx_hash: str) -> Optional[Transaction]:
        return db.query(self.model).filter(self.model.tx_hash == tx_hash).first()


transaction = CRUDTransaction(Transaction)
