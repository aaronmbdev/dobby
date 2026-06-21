from datetime import datetime, UTC

from sqlalchemy import select

from src.memory.database import SessionLocal
from src.summaries.models import Summary


class SummaryRepository:

    def save(self, summary_type: str, content: str) -> Summary:
        with SessionLocal() as session:
            summary = Summary(type=summary_type, content=content)
            session.add(summary)
            session.commit()
            session.refresh(summary)
            return summary

    def get_latest_unread(self) -> Summary | None:
        with SessionLocal() as session:
            result = session.execute(
                select(Summary)
                .where(Summary.read_at.is_(None))
                .order_by(Summary.created_at.desc())
                .limit(1)
            )
            return result.scalar_one_or_none()

    def mark_read(self, summary_id: int) -> None:
        with SessionLocal() as session:
            summary = session.get(Summary, summary_id)
            if summary:
                summary.read_at = datetime.now(UTC)
                session.commit()
