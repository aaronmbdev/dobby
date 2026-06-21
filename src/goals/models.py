from datetime import datetime, UTC
from typing import Literal

from sqlalchemy import Text, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base

GoalDomain = Literal["health", "finances", "diet", "general"]
GoalStatus = Literal["active", "completed", "abandoned"]


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(String(20), nullable=False)
    target: Mapped[str] = mapped_column(Text, nullable=False)
    deadline: Mapped[str | None] = mapped_column(String(10), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
