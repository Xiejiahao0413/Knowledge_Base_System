"""Chat API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.middleware.auth import require_api_key
from src.bootstrap import get_chat_service
from src.models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"], dependencies=[Depends(require_api_key)])


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    chat_service = get_chat_service()
    return chat_service.ask(question=request.question, session_id=request.session_id)

