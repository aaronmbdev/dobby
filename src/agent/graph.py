from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src.agent.checkpointer import checkpointer
from src.agent.nodes import agent_node
from src.agent.state import AgentState
from src.tools.registry import TOOLS


graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(TOOLS, handle_tool_errors=True))

graph.set_entry_point("agent")


def should_use_tools(state):
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"
    return END


graph.add_conditional_edges(
    "agent",
    should_use_tools,
    {"tools": "tools", END: END},
)

graph.add_edge("tools", "agent")

jarvis_graph = graph.compile(checkpointer=checkpointer)