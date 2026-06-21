from src.agent.context import build_context
from src.agent.prompts import DOBBY_SYSTEM
from src.agent.state import AgentState
from src.llm.openai import LLMClient
from src.tools.registry import TOOLS

llm = LLMClient(tools=TOOLS)


def agent_node(state: AgentState) -> AgentState:
    # System prompt and context injected at inference time, never stored in checkpointed state
    response = llm.invoke([DOBBY_SYSTEM, build_context()] + state["messages"])
    return {"messages": [response]}