from typing import List

from src.agent.graph import jarvis_graph
from src.common.models import Message


class ChatService:
    def chat(self, messages: List[Message]) -> str:
        result = jarvis_graph.invoke(
            {
                "messages": [
                    message.model_dump()
                    for message in messages
                ],
                "response": None
            }
        )

        return result["response"]