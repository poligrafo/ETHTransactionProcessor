from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.deps import get_db
from app.models.transaction_models import Transaction
from app.schemas.transaction_schemas import TransactionCreate

router = APIRouter()


@router.post("/", response_model=Transaction)
def create_transaction(
    transaction: TransactionCreate, db: Session = Depends(get_db)
):
    db_transaction = crud.transaction.get_by_tx_hash(db, tx_hash=transaction.tx_hash)
    if db_transaction:
        raise HTTPException(status_code=400, detail="Transaction already registered")
    return crud.transaction.create(db=db, obj_in=transaction)


@router.get("/", response_model=List[Transaction])
def read_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transactions = crud.transaction.get_multi(db, skip=skip, limit=limit)
    return transactions


@router.get("/{tx_hash}", response_model=Transaction)
def read_transaction(tx_hash: str, db: Session = Depends(get_db)):
    db_transaction = crud.transaction.get_by_tx_hash(db, tx_hash=tx_hash)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
