from fastapi import APIRouter, Depends, status

from src.schemas.account import AccountCancelIn, AccountIn, AccountOut
from src.security import login_required
from src.services.account import AccountService

account_router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)
account_service = AccountService()


@account_router.get(
    "/",
    summary="Listar contas",
    description="Retorna as contas cadastradas. Esta operação exige autenticação JWT.",
    response_model=list[AccountOut],
    dependencies=[Depends(login_required)],
)
async def read_accounts(limit: int, skip: int = 0):
    return await account_service.read_all(limit=limit, skip=skip)


@account_router.post(
    "/",
    summary="Criar conta",
    description="Cria uma conta vinculada ao user_id informado. Esta operação é pública.",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountOut,
)
async def create_account(account: AccountIn):
    return await account_service.create(account)


@account_router.patch(
    "/{account_id}/cancel",
    summary="Cancelar conta",
    description="Cancela uma conta ativa e registra o motivo e as observações da operação.",
    response_model=AccountOut,
    dependencies=[Depends(login_required)],
)
async def cancel_account(account_id: int, data: AccountCancelIn):
    return await account_service.cancel(account_id=account_id, data=data)
