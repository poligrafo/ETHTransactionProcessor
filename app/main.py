from fastapi import FastAPI
from app.db.session import engine
from app.models import transaction_models as transaction_model
from app.api.v1.endpoints import transactions as transaction_endpoint
from app.core.logging import logger

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")
    async with engine.begin() as conn:
        await conn.run_sync(transaction_model.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")

app.include_router(transaction_endpoint.router, prefix="/api/v1/transactions", tags=["transactions"])
