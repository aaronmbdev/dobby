from langgraph.graph import (
    StateGraph,
    END
)

from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)

from src.agent.state import AgentState
from src.agent.nodes import agent_node
from src.tools.registry import TOOLS


builder = StateGraph(AgentState)


builder.add_node(
    "agent",
    agent_node
)


builder.add_node(
    "tools",
    ToolNode(TOOLS)
)


builder.set_entry_point(
    "agent"
)


builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)


builder.add_edge(
    "tools",
    "agent"
)


jarvis_graph = builder.compile()