import sqlalchemy as sa

from src.database import metadata
from src.models.transaction_types import TransactionType

transactions = sa.Table(
    "transactions",
    metadata,
    sa.Column(
        "id",
        sa.Integer,
        primary_key=True,
    ),
    sa.Column(
        "account_id",
        sa.Integer,
        sa.ForeignKey("accounts.id"),
        nullable=False,
    ),
    sa.Column(
        "source_account_id",
        sa.Integer,
        sa.ForeignKey("accounts.id"),
        nullable=True,
    ),
    sa.Column(
        "destination_account_id",
        sa.Integer,
        sa.ForeignKey("accounts.id"),
        nullable=True,
    ),
    sa.Column(
        "type",
        sa.Enum(TransactionType, name="transaction_types"),
        nullable=False,
    ),
    sa.Column(
        "amount",
        sa.Numeric(10, 2),
        nullable=False,
    ),
    sa.Column(
        "timestamp",
        sa.TIMESTAMP(timezone=True),
        default=sa.func.now(),
    ),
)