from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.config import settings
from src.controllers.account import account_router
from src.controllers.transaction import transaction_router
from src.database import database
from src.exceptions import AccountInactiveError, AccountNotFoundError, BusinessError, InsufficientBalanceError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(account_router)
app.include_router(transaction_router)

print(settings.environment)


@app.get('/')
async def root():
    return {
        'message' : 'Hello World'
    }


@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": str(exc)})

@app.exception_handler(InsufficientBalanceError)
async def insufficient_balance_error_handler(request: Request, exc: InsufficientBalanceError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

@app.exception_handler(AccountInactiveError)
async def account_inactive_error_handler(request: Request, exc: AccountInactiveError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})
