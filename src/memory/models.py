from datetime import datetime

from sqlalchemy import Text, DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class Memory(Base):

    __tablename__ = "memories"


    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )


    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )