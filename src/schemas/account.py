from datetime import datetime

from pydantic import BaseModel, NonNegativeFloat

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