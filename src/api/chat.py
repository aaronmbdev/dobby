from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from src.api.models import ChatRequest, ChatResponse, HistoryResponse, ThreadListResponse
from src.memory.extractor import extract_and_save
from src.service.chat_service import ChatService
from src.service.thread_service import ThreadService

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


@router.get("/threads")
def list_threads(service: ThreadService = Depends()) -> ThreadListResponse:
    return ThreadListResponse(threads=service.list_threads())


@router.delete("/threads/{thread_id}", status_code=204)
def delete_thread(thread_id: str, service: ThreadService = Depends()) -> None:
    if not service.delete_thread(thread_id):
        raise HTTPException(status_code=404, detail=f"Thread '{thread_id}' not found.")
