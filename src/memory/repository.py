from sqlalchemy import select

from src.memory.database import SessionLocal
from src.memory.models import Memory


class MemoryRepository:


    def save(
        self,
        content: str
    ) -> None:

        with SessionLocal() as session:

            session.add(
                Memory(
                    content=content
                )
            )

            session.commit()


    def search(
        self,
        query: str
    ) -> list[str]:

        with SessionLocal() as session:

            result = session.execute(
                select(Memory)
                .where(
                    Memory.content.ilike(
                        f"%{query}%"
                    )
                )
            )

            return [
                memory.content
                for memory in result.scalars().all()
            ]