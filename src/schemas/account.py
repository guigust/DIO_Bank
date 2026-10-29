from datetime import datetime

from pydantic import BaseModel, Field, NonNegativeFloat

from src.models.account import CancellationReason


class AccountIn(BaseModel):
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
    cancellation: CancellationReason
    notes_cancellation: str = Field(min_length=1, max_length=150)
