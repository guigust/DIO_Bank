from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat

from src.models.transaction_types import TransactionType


class TransactionIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"account_id": 1, "amount": 100.0}],
        }
    )

    account_id: int
    amount: PositiveFloat


class TransferIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "source_account_id": 1,
                    "destination_account_id": 2,
                    "amount": 50.0,
                }
            ],
        }
    )

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