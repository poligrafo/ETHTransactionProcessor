from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import crud
from app.api.deps import get_db
from app.schemas.transaction_schemas import Transaction, TransactionCreate

router = APIRouter()


@router.post("/", response_model=Transaction)
async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)) -> Transaction:
    db_transaction = await crud.transaction.get_by_tx_hash(db, tx_hash=transaction.tx_hash)
    if db_transaction:
        raise HTTPException(status_code=400, detail="Transaction already registered")
    return await crud.transaction.create(db=db, obj_in=transaction)


@router.get("/", response_model=List[Transaction])
async def read_transactions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)) -> List[Transaction]:
    return await crud.transaction.get_multi(db, skip=skip, limit=limit)


@router.get("/{tx_hash}", response_model=Transaction)
async def read_transaction(tx_hash: str, db: AsyncSession = Depends(get_db)) -> Transaction:
    db_transaction = await crud.transaction.get_by_tx_hash(db, tx_hash=tx_hash)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
