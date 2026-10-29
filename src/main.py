from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.controllers.account import account_router
from src.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(account_router)

print(settings.environment)


@app.get('/')
async def root():
    return {
        'message' : 'Hello World'
    }
