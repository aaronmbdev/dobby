from typing import List

from pydantic import BaseModel

from src.common.models import Message


class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    message: List[Message]
    response: str