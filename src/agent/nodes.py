from src.agent.state import AgentState
from src.llm.openai import LLMClient
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