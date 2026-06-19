from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from src.agent.graph import jarvis_graph
from src.agent.prompts import DOBBY_SYSTEM
from src.common.models import Message


def _to_langchain_message(message: Message) -> BaseMessage:
    if message.role == "assistant":
        return AIMessage(content=message.content)
    return HumanMessage(content=message.content)


class ChatService:
    def chat(self, messages: list[Message]) -> str:
        result = jarvis_graph.invoke(
            {
                "messages": [
                    DOBBY_SYSTEM,
                    *[_to_langchain_message(m) for m in messages],
                ]
            }
        )
        return result["messages"][-1].content