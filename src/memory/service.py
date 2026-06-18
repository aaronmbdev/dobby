from src.memory.repository import MemoryRepository


class MemoryService:


    def __init__(self) -> None:
        self.repository = MemoryRepository()


    def save(
        self,
        information: str
    ) -> None:

        self.repository.save(
            information
        )


    def recall(
        self,
        query: str
    ) -> list[str]:

        return self.repository.search(
            query
        )