from databases.interfaces import Record

from src.database import database
from src.models.account import accounts
from src.schemas.account import AccountIn


class AccountService:
    async def read_all(self, limit: int, skip: int = 0) -> list[Record]:
        query = accounts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, account: AccountIn) -> Record:
        command = accounts.insert().values(
            user_id=account.user_id,
            balance=0,
            active=True,
        )
        account_id = await database.execute(command)

        query = accounts.select().where(accounts.c.id == account_id)
        record = await database.fetch_one(query)
        if record is None:
            raise RuntimeError('Conta criada, mas não encontrada')
        return record