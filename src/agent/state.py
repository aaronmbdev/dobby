from typing import TypedDict


from typing import TypedDict, List


class Message(TypedDict):
    role: str
    content: str


class AgentState(TypedDict):
    messages: List[Message]
    response: str | None