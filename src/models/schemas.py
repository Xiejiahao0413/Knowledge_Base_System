"""API-focused schema wrappers."""

from __future__ import annotations

from pydantic import BaseModel

from src.models.chat import ChatRequest, ChatResponse
from src.models.document import DocumentPreview, KnowledgeBaseStats, UploadResult


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str


__all__ = [
    "ChatRequest",
    "ChatResponse",
    "DocumentPreview",
    "HealthResponse",
    "KnowledgeBaseStats",
    "UploadResult",
]

