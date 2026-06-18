from src.agent.state import AgentState
from src.llm.openai import LLMClient
from src.tools.memory import memory_service
from src.tools.registry import TOOLS

llm = LLMClient().with_tools(TOOLS)

def agent_node(
    state: AgentState
) -> AgentState:

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [
            response
        ]
    }


def memory_node(state):

    last_message = state["messages"][-1]

    memories = memory_service.recall(
        last_message.content
    )

    if not memories:
        return state

    context = "\n".join(memories)

    return {
        "messages": [
            SystemMessage(
                content=f"""
You have the following memories about the user:

{context}

Use them when relevant.
"""
            )
        ]
    }