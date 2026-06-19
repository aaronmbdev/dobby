from langchain_openai import ChatOpenAI

from src.config.settings import settings


class LLMClient:

    def __init__(self, tools=None):
        client = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0,
        )
        self._llm = client.bind_tools(tools) if tools else client

    def invoke(self, messages):
        return self._llm.invoke(messages)