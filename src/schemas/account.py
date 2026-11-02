from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, NonNegativeFloat

from src.models.account import CancellationReason


class AccountIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"user_id": 123}],
        }
    )

    user_id: int


class AccountOut(BaseModel):
    id: int
    user_id: int
    active: bool
    balance: NonNegativeFloat
    created_at: datetime
    cancellation: CancellationReason | None = None
    notes_cancellation: str | None = None
    cancelled_at: datetime | None = None


class AccountCancelIn(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "cancellation": "request_holder",
                    "notes_cancellation": "Solicitação do titular",
                }
            ],
        }
    )

    cancellation: CancellationReason
    notes_cancellation: str = Field(min_length=1, max_length=150)
