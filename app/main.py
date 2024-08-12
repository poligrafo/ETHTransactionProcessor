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


