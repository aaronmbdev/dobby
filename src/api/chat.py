from fastapi import APIRouter

from src.api.models import ChatRequest, ChatResponse
from src.service.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest) -> ChatResponse:
    service = ChatService()
    response = service.chat(request.messages)
    return ChatResponse(message=request.messages, response=response)
