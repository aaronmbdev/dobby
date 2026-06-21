from langchain_core.messages import HumanMessage

from src.agent.graph import jarvis_graph


class ChatService:
    def chat(self, message: str, thread_id: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        result = jarvis_graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )
        return result["messages"][-1].content