from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.api.deps import get_db
from app.core.cache import get_from_cache, set_to_cache
from app.models import Transaction
from app.schemas.transaction_schemas import TransactionOut, TransactionStats
from app.services.ethereum_servises import fetch_and_save_latest_transactions
from app.crud.transaction_crud import get_transactions, get_transaction_by_hash, get_transaction_stats
from app.celery.tasks import fetch_and_save_transactions_task

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

CACHE_EXPIRE_IN_SECONDS = 24 * 60 * 60  # 24 hours


@router.get("/", response_model=List[TransactionOut])
async def list_transactions(
        skip: int = 0,
        limit: int = 50,
        from_address: Optional[str] = None,
        to_address: Optional[str] = None,
        block_number: Optional[int] = None,
        db: AsyncSession = Depends(get_db)
):
    cache_key = f"transactions_{skip}_{limit}_{from_address}_{to_address}_{block_number}"
    cached_data = await get_from_cache(cache_key)
    if cached_data:
        logger.info(f"Returning cached data for {cache_key}")
        return cached_data

    transactions = await get_transactions(
        db, skip=skip, limit=limit, from_address=from_address, to_address=to_address, block_number=block_number
    )
    logger.info(f"Fetched {len(transactions)} transactions")

    await set_to_cache(cache_key, transactions, expire=CACHE_EXPIRE_IN_SECONDS)
    return transactions


@router.get("/stats", response_model=TransactionStats)
async def transaction_stats(db: AsyncSession = Depends(get_db)):
    cache_key = "transaction_stats"
    cached_data = await get_from_cache(cache_key)
    if cached_data:
        logger.info(f"Returning cached stats")
        return cached_data

    stats = await get_transaction_stats(db)
    logger.info(f"Transaction stats: {stats}")

    await set_to_cache(cache_key, stats, expire=CACHE_EXPIRE_IN_SECONDS)
    return stats


@router.get("/{tx_hash}", response_model=TransactionOut)
async def get_transaction(tx_hash: str, db: AsyncSession = Depends(get_db)):
    cache_key = f"transaction_{tx_hash}"
    cached_data = await get_from_cache(cache_key)
    if cached_data:
        logger.info(f"Returning cached transaction {tx_hash}")
        return cached_data

    transaction = await get_transaction_by_hash(db, tx_hash)
    if not transaction:
        logger.warning(f"Transaction not found: {tx_hash}")
        raise HTTPException(status_code=404, detail="Transaction not found")

    logger.info(f"Fetched transaction {tx_hash}")

    await set_to_cache(cache_key, transaction, expire=CACHE_EXPIRE_IN_SECONDS)
    return transaction


@router.post("/update/")
async def update_transactions():
    fetch_and_save_transactions_task.delay()
    logger.info("Triggered transaction update task")
    return {"message": "Updating transactions in the background"}

