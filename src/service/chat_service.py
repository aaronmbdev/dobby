from typing import List

from langchain_core.messages import HumanMessage

from src.agent.graph import jarvis_graph
from src.common.models import Message


class ChatService:
    def chat(
        self,
        messages: list[Message]
    ) -> str:

        result = jarvis_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=message.content
                    )
                    for message in messages
                ]
            }
        )

        return result["messages"][-1].content