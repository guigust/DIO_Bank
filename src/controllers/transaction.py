from fastapi import APIRouter, status

from src.schemas.transaction import TransactionIn, TransactionOut, TransferIn
from src.services.transaction import TransactionService

transaction_router = APIRouter(prefix="/transactions")
transaction_service = TransactionService()


@transaction_router.post(
    "/deposit",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def deposit_transaction(data: TransactionIn):
    return await transaction_service.deposit(data)

@transaction_router.post(
    "/withdraw",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def withdraw_transaction(data: TransactionIn):
    return await transaction_service.withdraw(data)

@transaction_router.post(
    "/transfer",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def transfer_transaction(data: TransferIn):
    return await transaction_service.transfer(data)


@transaction_router.post(
    "/pix",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def pix_transaction(data: TransferIn):
    return await transaction_service.pix(data)


@transaction_router.post(
    "/ted",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def ted_transaction(data: TransferIn):
    return await transaction_service.ted(data)

@transaction_router.get(
    "/{account_id}/statement",
    response_model=list[TransactionOut],
)
async def transaction_statement(account_id: int):
    return await transaction_service.statement(account_id)
