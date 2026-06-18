from langchain_openai import ChatOpenAI

from src.config.settings import settings


class LLMClient:

    def __init__(self):
        self.client = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0,
        )

    def with_tools(self, tools):
        return self.client.bind_tools(tools)