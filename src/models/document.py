"""Document-related data models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UploadRequest(BaseModel):
    filename: str
    content: str
    operator: str = "system"


class UploadResult(BaseModel):
    success: bool
    message: str
    skipped: bool = False
    chunk_count: int = 0
    document_md5: str | None = None
    filename: str | None = None


class DocumentPreview(BaseModel):
    filename: str
    encoding: str
    size_bytes: int
    preview: str = Field(description="Preview content for UI/API display")


class KnowledgeBaseStats(BaseModel):
    collection_name: str
    document_count: int
    storage_path: str

