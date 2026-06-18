from langchain.tools import tool

from src.memory.service import MemoryService


memory_service = MemoryService()


@tool(
    description="Save an important user memory."
)
def remember(
    information: str
) -> str:

    memory_service.save(
        information
    )

    return "Memory saved."


@tool(
    description="Search memories about the user."
)
def recall(
    query: str
) -> str:

    memories = memory_service.recall(
        query
    )

    if not memories:
        return "No memories found."

    return "\n".join(memories)