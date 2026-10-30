"""add transaction account endpoints

Revision ID: 839ae98fa52d
Revises: c98432daa4b4
Create Date: 2026-10-30 12:56:09.639469

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '839ae98fa52d'
down_revision: str | Sequence[str] | None = 'c98432daa4b4'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "source_account_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.add_column(
            sa.Column(
                "destination_account_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.create_foreign_key(
            "fk_transactions_source_account_id_accounts",
            "accounts",
            ["source_account_id"],
            ["id"],
        )
        batch_op.create_foreign_key(
            "fk_transactions_destination_account_id_accounts",
            "accounts",
            ["destination_account_id"],
            ["id"],
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("transactions", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_transactions_destination_account_id_accounts",
            type_="foreignkey",
        )
        batch_op.drop_constraint(
            "fk_transactions_source_account_id_accounts",
            type_="foreignkey",
        )
        batch_op.drop_column("destination_account_id")
        batch_op.drop_column("source_account_id")
