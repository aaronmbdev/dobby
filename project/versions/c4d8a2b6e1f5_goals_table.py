"""goals table

Revision ID: c4d8a2b6e1f5
Revises: a3f92c1d4e87
Create Date: 2026-06-20 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "c4d8a2b6e1f5"
down_revision: Union[str, Sequence[str], None] = "a3f92c1d4e87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("domain", sa.String(20), nullable=False),
        sa.Column("target", sa.Text(), nullable=False),
        sa.Column("deadline", sa.String(10), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("goals")
