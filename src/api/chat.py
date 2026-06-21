from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.models import ChatRequest, ChatResponse
from src.memory.extractor import extract_and_save
from src.service.chat_service import ChatService

router = APIRouter()


@router.post("/chat")
def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    service: ChatService = Depends(),
) -> ChatResponse:
    response = service.chat(request.message, request.thread_id)
    background_tasks.add_task(extract_and_save, request.message, response)
    return ChatResponse(response=response)
