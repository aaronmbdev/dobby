from sqlalchemy import select

from src.memory.database import SessionLocal
from src.memory.models import Memory


class MemoryRepository:

    def save(self, content: str, embedding: list[float]) -> None:
        with SessionLocal() as session:
            session.add(Memory(content=content, embedding=embedding))
            session.commit()

    def search(self, embedding: list[float], limit: int = 5) -> list[str]:
        with SessionLocal() as session:
            result = session.execute(
                select(Memory)
                .order_by(Memory.embedding.cosine_distance(embedding))
                .limit(limit)
            )
            return [memory.content for memory in result.scalars().all()]