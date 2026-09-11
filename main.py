from fastapi import FastAPI
from api.routers import portfolios, transactions
from core.database import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(portfolios.router)
app.include_router(transactions.router)