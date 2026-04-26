"""Knowledge base ingestion and stats API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, UploadFile

from src.api.middleware.auth import require_api_key
from src.bootstrap import get_document_service, get_knowledge_service
from src.models.document import KnowledgeBaseStats, UploadResult

router = APIRouter(
    prefix="/api/knowledge",
    tags=["knowledge"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/stats", response_model=KnowledgeBaseStats)
def knowledge_stats() -> KnowledgeBaseStats:
    return get_knowledge_service().get_stats()


@router.post("/upload", response_model=UploadResult)
async def upload_document(
    file: UploadFile = File(...),
    operator: str = Form(default="system"),
) -> UploadResult:
    content = await file.read()
    document_service = get_document_service()
    request = document_service.read_bytes(
        filename=file.filename or "uploaded.txt",
        content=content,
        operator=operator,
    )
    return get_knowledge_service().upload_text(request)
