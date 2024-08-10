# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# from sqlalchemy import func
# from typing import List
#
# from app.api.deps import get_db
# from app.models.transaction_models import Transaction
# from app.schemas.transaction_schemas import Transaction as TransactionSchema, TransactionCreate
# from app.celery.tasks import fetch_and_save_transactions_task
#
# router = APIRouter()
#
#
# @router.get("/transactions", response_model=List[TransactionSchema])
# async def get_transactions(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> List[TransactionSchema]:
#     result = await db.execute(select(Transaction).offset(skip).limit(limit))
#     transactions = result.scalars().all()
#     return list(transactions)
#
#
# @router.post("/transactions", response_model=TransactionSchema)
# async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db)) -> TransactionSchema:
#     db_transaction = Transaction(**transaction.dict())
#     db.add(db_transaction)
#     await db.commit()
#     await db.refresh(db_transaction)
#     return db_transaction
#
#
# @router.get("/transactions/stats")
# async def get_transaction_stats(db: AsyncSession = Depends(get_db)) -> dict:
#     total_count_result = await db.execute(select(func.count(Transaction.id)))
#     avg_gas_price_result = await db.execute(select(func.avg(Transaction.gas_price)))
#     total_count = total_count_result.scalar()
#     avg_gas_price = avg_gas_price_result.scalar()
#     return {
#         "total_count": total_count,
#         "avg_gas_price": avg_gas_price
#     }
#    }
#
#
# @router.get("/transactions/{tx_hash}", response_model=TransactionSchema)
# async def get_transaction(tx_hash: str, db: AsyncSession = Depends(get_db)) -> TransactionSchema:
#     result = await db.execute(select(Transaction).filter(Transaction.hash == tx_hash))
#     transaction = result.scalar_one_or_none()
#     if transaction is None:
#         raise HTTPException(status_code=404, detail="Transaction not found")
#     return transaction
#
#
# @router.post("/update-transactions/")
# async def update_transactions():
#     fetch_and_save_transactions_task.delay()
#     return {"message": "Updating transactions in the background"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.deps import get_db
from app.schemas.transaction_schemas import TransactionOut, TransactionStats
from app.services.ethereum_servises import fetch_and_save_latest_transactions
from app.crud.transaction_crud import get_transactions, get_transaction_by_hash, get_transaction_stats
from app.celery.tasks import fetch_and_save_transactions_task

import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[TransactionOut])
async def list_transactions(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    transactions = await get_transactions(db, skip=skip, limit=limit)
    logger.info(f"Fetched {len(transactions)} transactions")
    return transactions


@router.get("/stats", response_model=TransactionStats)
async def transaction_stats(db: AsyncSession = Depends(get_db)):
    stats = await get_transaction_stats(db)
    logger.info(f"Transaction stats: {stats}")
    return stats


@router.get("/{tx_hash}", response_model=TransactionOut)
async def get_transaction(tx_hash: str, db: AsyncSession = Depends(get_db)):
    transaction = await get_transaction_by_hash(db, tx_hash)
    if not transaction:
        logger.warning(f"Transaction not found: {tx_hash}")
        raise HTTPException(status_code=404, detail="Transaction not found")
    logger.info(f"Fetched transaction {tx_hash}")
    return transaction


@router.post("/update/")
async def update_transactions():
    fetch_and_save_transactions_task.delay()
    logger.info("Triggered transaction update task")
    return {"message": "Updating transactions in the background"}

