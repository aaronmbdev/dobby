from src.agent.state import AgentState
from src.llm.openai import LLMClient


def answer_node(state: AgentState) -> AgentState:
    llm = LLMClient()
    response = llm.chat(
        state["messages"]
    )

    return {
        "messages": [
            response
        ]
    }