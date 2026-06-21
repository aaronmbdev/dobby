from datetime import datetime, UTC

from pgvector.sqlalchemy import Vector
from sqlalchemy import Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base

EMBEDDING_DIM = 1536


class Memory(Base):

    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(EMBEDDING_DIM),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )