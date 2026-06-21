from fastapi import APIRouter, BackgroundTasks, Depends

from src.api.models import ChatRequest, ChatResponse, HistoryResponse
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


@router.get("/chat/history")
def get_history(
    thread_id: str = "default",
    service: ChatService = Depends(),
) -> HistoryResponse:
    messages = service.get_history(thread_id)
    return HistoryResponse(thread_id=thread_id, messages=messages)
