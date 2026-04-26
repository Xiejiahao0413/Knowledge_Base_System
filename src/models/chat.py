"""Chat-related data models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourceSnippet(BaseModel):
    content: str
    metadata: dict = Field(default_factory=dict)


class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[SourceSnippet] = Field(default_factory=list)

