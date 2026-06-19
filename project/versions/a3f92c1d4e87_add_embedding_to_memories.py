"""add embedding to memories

Revision ID: a3f92c1d4e87
Revises: 79081dc21b8b
Create Date: 2026-06-18 21:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

from src.memory.models import EMBEDDING_DIM

# revision identifiers, used by Alembic.
revision: str = "a3f92c1d4e87"
down_revision: Union[str, Sequence[str], None] = "79081dc21b8b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column(
        "memories",
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=True),
    )


def downgrade():
    op.drop_column("memories", "embedding")
