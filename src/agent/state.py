from typing import TypedDict

from langchain_core.messages import BaseMessage


class Message(TypedDict):
    role: str
    content: str


class AgentState(TypedDict):
    messages: list[BaseMessage]