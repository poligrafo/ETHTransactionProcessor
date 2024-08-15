from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from app.api.deps import get_db
from app.schemas.transaction_schemas import TransactionOut, TransactionStats, TransactionQueryParams
from app.db.transaction_crud import get_transactions, get_transaction_by_hash, get_transaction_stats
from app.core.cache import CacheHandler

import logging

logger = logging.getLogger(__name__)

router = APIRouter()

CACHE_EXPIRE_IN_SECONDS = 24 * 60 * 60  # 24 hours


@router.get("/", response_model=List[TransactionOut])
async def list_transactions(
        params: TransactionQueryParams = Depends(),
        cache: CacheHandler = Depends(CacheHandler)) -> List[Dict[str, Any]]:
    cache_key = f"transactions_{params.skip}_{params.limit}_{params.from_address}_{params.to_address}_{params.block_number}"
    cached_data = await cache.get_from_cache(cache_key)

    if cached_data:
        logger.info(f"Returning cached data for {cache_key}")
        return cached_data

    transactions = await get_transactions(
        params.db, skip=params.skip, limit=params.limit,
        from_address=params.from_address, to_address=params.to_address,
        block_number=params.block_number
    )
    logger.info(f"Fetched {len(transactions)} transactions")

    transactions_data = [TransactionOut.from_orm(transaction).dict() for transaction in transactions]

    await cache.set_to_cache(cache_key, transactions_data, expire=CACHE_EXPIRE_IN_SECONDS)
    return transactions_data


@router.get("/stats", response_model=TransactionStats)
async def transaction_stats(
        db: AsyncSession = Depends(get_db),
        cache: CacheHandler = Depends(CacheHandler)) -> TransactionStats:
    cache_key = "transaction_stats"
    cached_data = await cache.get_from_cache(cache_key)

    if cached_data:
        logger.info(f"Returning cached stats")
        return TransactionStats(**cached_data)

    stats = await get_transaction_stats(db)
    logger.info(f"Transaction stats: {stats}")

    await cache.set_to_cache(cache_key, stats.dict(), expire=CACHE_EXPIRE_IN_SECONDS)
    return stats


@router.get("/{tx_hash}", response_model=TransactionOut)
async def get_transaction(
        tx_hash: str,
        db: AsyncSession = Depends(get_db),
        cache: CacheHandler = Depends(CacheHandler)) -> TransactionOut:
    cache_key = f"transaction_{tx_hash}"
    cached_data = await cache.get_from_cache(cache_key)

    if cached_data:
        logger.info(f"Returning cached transaction {tx_hash}")
        return TransactionOut(**cached_data)

    transaction = await get_transaction_by_hash(db, tx_hash)
    if not transaction:
        logger.warning(f"Transaction not found: {tx_hash}")
        raise HTTPException(status_code=404, detail="Transaction not found")

    logger.info(f"Fetched transaction {tx_hash}")

    transaction_out = TransactionOut.from_orm(transaction)
    await cache.set_to_cache(cache_key, transaction_out.dict(), expire=CACHE_EXPIRE_IN_SECONDS)

    return transaction_out
