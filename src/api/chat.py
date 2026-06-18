from fastapi import APIRouter, Depends

from src.api.models import ChatRequest, ChatResponse
from src.service.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
def chat(request: ChatRequest, service: ChatService = Depends()) -> ChatResponse:
    response = service.chat(request.messages)
    return ChatResponse(response=response)
