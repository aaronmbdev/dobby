from src.llm.embeddings import embed
from src.memory.repository import MemoryRepository


class MemoryService:

    def __init__(self) -> None:
        self.repository = MemoryRepository()

    def save(self, information: str) -> None:
        embedding = embed(information)
        self.repository.save(information, embedding)

    def recall(self, query: str) -> list[str]:
        embedding = embed(query)
        return self.repository.search(embedding)