from langchain_core.messages import AIMessage, BaseMessage
from openai import OpenAI

from src.config.settings import settings


class LLMClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )


    def chat(
        self,
        messages: list[BaseMessage]
    ) -> AIMessage:

        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": self._map_role(message),
                    "content": message.content
                }
                for message in messages
            ]
        )

        return AIMessage(
            content=response.choices[0].message.content
        )


    def _map_role(
        self,
        message: BaseMessage
    ) -> str:

        if isinstance(message, AIMessage):
            return "assistant"

        return "user"