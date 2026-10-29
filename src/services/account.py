from datetime import UTC, datetime

from databases.interfaces import Record

from src.database import database
from src.exceptions import AccountInactiveError, AccountNotFoundError
from src.models.account import accounts
from src.schemas.account import AccountCancelIn, AccountIn


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

    async def cancel(self, account_id: int, data: AccountCancelIn) -> Record:
        query = accounts.select().where(accounts.c.id == account_id)

        async with database.transaction():
            record = await database.fetch_one(query)

            if record is None:
                raise AccountNotFoundError("Conta não encontrada")

            if not record["active"]:
                raise AccountInactiveError("A conta já está inativa")

            update = (
                accounts.update()
                .where(accounts.c.id == account_id)
                .values(
                    active=False,
                    balance=0,
                    cancellation=data.cancellation,
                    notes_cancellation=data.notes_cancellation,
                    cancelled_at=datetime.now(UTC),
                )
            )

            await database.execute(update)

            updated_record = await database.fetch_one(query)

            if updated_record is None:
                raise AccountNotFoundError("Conta não encontrada após atualização")

            return updated_record