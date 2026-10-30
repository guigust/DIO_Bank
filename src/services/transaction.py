from databases.interfaces import Record

from src.database import database
from src.exceptions import (
    AccountInactiveError,
    AccountNotFoundError,
    BusinessError,
    InsufficientBalanceError,
)
from src.models.account import accounts
from src.models.transaction import transactions
from src.models.transaction_types import TransactionType
from src.schemas.transaction import TransactionIn, TransferIn


class TransactionService:
    async def deposit(self, data: TransactionIn) -> Record:
        account_query = accounts.select().where(accounts.c.id == data.account_id)

        async with database.transaction():
            account = await database.fetch_one(account_query)

            if account is None:
                raise AccountNotFoundError("Conta não encontrada")

            if not account["active"]:
                raise AccountInactiveError("A conta já está inativa")

            update_account = (
                accounts.update()
                .where(accounts.c.id == data.account_id)
                .values(balance=accounts.c.balance + data.amount)
            )

            await database.execute(update_account)

            insert_transaction = transactions.insert().values(
                account_id=data.account_id,
                type=TransactionType.DEPOSIT,
                amount=data.amount,
            )

            transaction_id = await database.execute(insert_transaction)

            transaction_query = transactions.select().where(
                transactions.c.id == transaction_id
            )

            transaction = await database.fetch_one(transaction_query)

            if transaction is None:
                raise RuntimeError(
                    "Depósito realizado, mas lançamento não encontrado"
                )

            return transaction

    async def withdraw(self, data: TransactionIn) -> Record:
        account_query = accounts.select().where(accounts.c.id == data.account_id)

        async with database.transaction():
            account = await database.fetch_one(account_query)

            if account is None:
                raise AccountNotFoundError("Conta não encontrada")

            if not account["active"]:
                raise AccountInactiveError("A conta já está inativa")

            if account["balance"] < data.amount:
                raise InsufficientBalanceError("Saldo insuficiente")

            update_account = (
                accounts.update()
                .where(accounts.c.id == data.account_id)
                .values(balance=accounts.c.balance - data.amount)
            )

            await database.execute(update_account)

            insert_transaction = transactions.insert().values(
                account_id=data.account_id,
                type=TransactionType.WITHDRAWAL,
                amount=data.amount,
            )

            transaction_id = await database.execute(insert_transaction)

            transaction_query = transactions.select().where(
                transactions.c.id == transaction_id
            )

            transaction = await database.fetch_one(transaction_query)

            if transaction is None:
                raise RuntimeError(
                    "Saque realizado, mas lançamento não encontrado"
                )

            return transaction

    async def _transfer_between_accounts(
        self,
        data: TransferIn,
        transaction_type: TransactionType,
    ) -> Record:
        if data.source_account_id == data.destination_account_id:
            raise BusinessError(
                "A conta de origem deve ser diferente da conta de destino"
            )

        source_query = accounts.select().where(
            accounts.c.id == data.source_account_id
        )
        destination_query = accounts.select().where(
            accounts.c.id == data.destination_account_id
        )

        async with database.transaction():
            source_account = await database.fetch_one(source_query)
            destination_account = await database.fetch_one(destination_query)

            if source_account is None:
                raise AccountNotFoundError("Conta de origem não encontrada")

            if destination_account is None:
                raise AccountNotFoundError("Conta de destino não encontrada")

            if not source_account["active"]:
                raise AccountInactiveError("A conta de origem está inativa")

            if not destination_account["active"]:
                raise AccountInactiveError("A conta de destino está inativa")

            if source_account["balance"] < data.amount:
                raise InsufficientBalanceError("Saldo insuficiente")

            update_source = (
                accounts.update()
                .where(accounts.c.id == data.source_account_id)
                .values(balance=accounts.c.balance - data.amount)
            )

            update_destination = (
                accounts.update()
                .where(accounts.c.id == data.destination_account_id)
                .values(balance=accounts.c.balance + data.amount)
            )

            await database.execute(update_source)
            await database.execute(update_destination)

            insert_transaction = transactions.insert().values(
                account_id=data.source_account_id,
                source_account_id=data.source_account_id,
                destination_account_id=data.destination_account_id,
                type=transaction_type,
                amount=data.amount,
            )

            transaction_id = await database.execute(insert_transaction)

            transaction_query = transactions.select().where(
                transactions.c.id == transaction_id
            )

            transaction = await database.fetch_one(transaction_query)

            if transaction is None:
                raise RuntimeError(
                    "Operação entre contas realizada, mas lançamento não encontrado"
                )

            return transaction

    async def transfer(self, data: TransferIn) -> Record:
        return await self._transfer_between_accounts(
            data=data,
            transaction_type=TransactionType.TRANSFER,
        )

    async def pix(self, data: TransferIn) -> Record:
        return await self._transfer_between_accounts(
            data=data,
            transaction_type=TransactionType.PIX,
        )

    async def ted(self, data: TransferIn) -> Record:
        return await self._transfer_between_accounts(
            data=data,
            transaction_type=TransactionType.TED,
        )

    async def statement(self, account_id: int) -> list[Record]:
        account_query = accounts.select().where(accounts.c.id == account_id)
        account = await database.fetch_one(account_query)

        if account is None:
            raise AccountNotFoundError("Conta não encontrada")

        statement_query = (
            transactions.select()
            .where(
                (transactions.c.account_id == account_id)
                | (transactions.c.source_account_id == account_id)
                | (transactions.c.destination_account_id == account_id)
            )
            .order_by(
                transactions.c.timestamp.desc(),
                transactions.c.id.desc(),
            )
        )

        return await database.fetch_all(statement_query)
