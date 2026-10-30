from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat

from src.models.transaction_types import TransactionType


class TransactionIn(BaseModel):
    account_id: int
    amount: PositiveFloat


class TransferIn(BaseModel):
    source_account_id: int
    destination_account_id: int
    amount: PositiveFloat


class TransactionOut(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: int
    account_id: int
    source_account_id: int | None = None
    destination_account_id: int | None = None
    type: TransactionType
    amount: PositiveFloat
    timestamp: datetime