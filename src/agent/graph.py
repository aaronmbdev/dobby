from langgraph.graph import StateGraph, START, END

from src.agent.state import AgentState
from src.agent.nodes import answer_node


builder = StateGraph(AgentState)


builder.add_node(
    "answer",
    answer_node
)


builder.add_edge(
    START,
    "answer"
)


builder.add_edge(
    "answer",
    END
)


jarvis_graph = builder.compile()