# from fastapi import FastAPI
# from app.db.session import engine
# from app.models import transaction_models as transaction_model
# from app.api.v1.endpoints import transactions as transaction_endpoint
# from app.core.logging import logger
#
# app = FastAPI()
#
#
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up the application...")
#     async with engine.begin() as conn:
#         await conn.run_sync(transaction_model.Base.metadata.create_all)
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     logger.info("Shutting down the application...")
#
# app.include_router(transaction_endpoint.router, prefix="/api/v1/transactions", tags=["transactions"])


# from fastapi import FastAPI
# from app.core.logging import logger
# from app.api.v1.endpoints import transactions
#
# app = FastAPI()
#
#
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Starting up the application...")
#
# app.include_router(transactions.router, prefix="/api/v1")
#
#
# @app.get("/")
# async def read_root():
#     logger.info("Handling request to root endpoint")
#     return {"status": "Service is running", "version": "1.0.0"}


from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import aioredis
from fastapi_cache.decorator import cache

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/cached-data")
@cache(expire=60)
async def get_cached_data():
    return {"data": "This is cached"}

