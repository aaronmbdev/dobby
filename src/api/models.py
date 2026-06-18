from pydantic import BaseModel

from src.common.models import Message


class ChatRequest(BaseModel):
    messages: list[Message]


class ChatResponse(BaseModel):
    response: str