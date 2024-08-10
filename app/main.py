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


import logging
from fastapi import FastAPI
from app.api.v1.endpoints.transactions import router as transactions_router
from app.core.logging import setup_logging
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")

app.include_router(transactions_router, prefix="/api/v1/transactions", tags=["transactions"])


@app.get("/")
async def root():
    logger.info("Handling root endpoint")
    return {"message": "Ethereum Transaction Processor API"}


