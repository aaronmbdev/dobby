from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
)


from src.config.settings import settings

class LLMClient:

    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.openai_api_key,
            temperature=0
        )

    def with_tools(self, tools):
        return self.client.bind_tools(tools)


    def chat(
        self,
        messages: list[BaseMessage],
        tools=None
    ) -> AIMessage:

        llm = self.client

        if tools:
            llm = llm.bind_tools(tools)

        return llm.invoke(messages)


    def _map_role(
        self,
        message: BaseMessage
    ) -> str:

        if isinstance(message, AIMessage):
            return "assistant"

        return "user"