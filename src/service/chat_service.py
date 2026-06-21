from langchain_core.messages import HumanMessage, AIMessage

from src.agent.graph import jarvis_graph
from src.api.models import ChatMessage


class ChatService:
    def chat(self, message: str, thread_id: str) -> str:
        config = {"configurable": {"thread_id": thread_id}}
        result = jarvis_graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )
        return result["messages"][-1].content

    def get_history(self, thread_id: str) -> list[ChatMessage]:
        config = {"configurable": {"thread_id": thread_id}}
        state = jarvis_graph.get_state(config)
        messages = []
        for msg in state.values.get("messages", []):
            if isinstance(msg, HumanMessage):
                messages.append(ChatMessage(role="user", content=msg.content))
            elif isinstance(msg, AIMessage) and not msg.tool_calls:
                messages.append(ChatMessage(role="assistant", content=msg.content))
        return messages