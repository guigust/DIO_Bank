from fastapi import APIRouter, Depends, status

from src.schemas.transaction import TransactionIn, TransactionOut, TransferIn
from src.security import login_required
from src.services.transaction import TransactionService

transaction_router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
    dependencies=[Depends(login_required)],
)
transaction_service = TransactionService()


@transaction_router.post(
    "/deposit",
    summary="Depositar",
    description="Adiciona um valor positivo ao saldo da conta autenticada.",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def deposit_transaction(data: TransactionIn):
    return await transaction_service.deposit(data)

@transaction_router.post(
    "/withdraw",
    summary="Sacar",
    description="Retira um valor positivo quando a conta possui saldo suficiente.",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def withdraw_transaction(data: TransactionIn):
    return await transaction_service.withdraw(data)

@transaction_router.post(
    "/transfer",
    summary="Transferir entre contas",
    description="Transfere um valor positivo entre duas contas ativas do mesmo banco.",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def transfer_transaction(data: TransferIn):
    return await transaction_service.transfer(data)


@transaction_router.post(
    "/pix",
    summary="Realizar PIX interno",
    description="Realiza um PIX interno entre duas contas ativas do mesmo banco.",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def pix_transaction(data: TransferIn):
    return await transaction_service.pix(data)


@transaction_router.post(
    "/ted",
    summary="Realizar TED interno",
    description="Realiza uma TED interna entre duas contas ativas do mesmo banco.",
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionOut,
)
async def ted_transaction(data: TransferIn):
    return await transaction_service.ted(data)

@transaction_router.get(
    "/{account_id}/statement",
    summary="Consultar extrato",
    description="Retorna o extrato de transações de uma conta existente.",
    response_model=list[TransactionOut],
)
async def transaction_statement(account_id: int):
    return await transaction_service.statement(account_id)
