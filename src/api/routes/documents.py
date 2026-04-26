"""Document preview API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from src.api.middleware.auth import require_api_key
from src.bootstrap import get_document_service
from src.models.document import DocumentPreview

router = APIRouter(
    prefix="/api/documents",
    tags=["documents"],
    dependencies=[Depends(require_api_key)],
)


@router.post("/preview", response_model=DocumentPreview)
async def preview_document(file: UploadFile = File(...)) -> DocumentPreview:
    content = await file.read()
    document_service = get_document_service()
    return document_service.preview_bytes(
        filename=file.filename or "uploaded.txt",
        content=content,
    )
