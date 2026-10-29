from fastapi import APIRouter, status

from src.schemas.account import AccountCancelIn, AccountIn, AccountOut
from src.services.account import AccountService

account_router = APIRouter(prefix="/accounts")
account_service = AccountService()


@account_router.get("/", response_model=list[AccountOut])
async def read_accounts(limit: int, skip: int = 0):
    return await account_service.read_all(limit=limit, skip=skip)


@account_router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
async def create_account(account: AccountIn):
    return await account_service.create(account)

@account_router.patch("/{account_id}/cancel", response_model=AccountOut)
async def cancel_account(account_id: int, data: AccountCancelIn):
    return await account_service.cancel(account_id=account_id, data=data)
