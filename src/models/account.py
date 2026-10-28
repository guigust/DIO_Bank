from enum import Enum

import sqlalchemy as sa

from src.database import metadata


class CancellationReason(str, Enum):
    REQUEST_HOLDER = "request_holder"
    OTHER_REASONS = "other_reasons"
    

accounts = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("user_id", sa.Integer, nullable=False, index=True),
    sa.Column('active', sa.Boolean, nullable=False, default=True, server_default=sa.true()),
    sa.Column("balance", sa.Numeric(10, 2), nullable=False, default=0),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
    sa.Column('cancellation', sa.Enum(CancellationReason, name='cancellation_reason'), nullable=True),
    sa.Column('notes_cancellation', sa.String(150), nullable=True, default=None),
    sa.Column("cancelled_at", sa.TIMESTAMP(timezone=True), default=None, nullable=True),
)
