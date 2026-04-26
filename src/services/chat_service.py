"""Chat service powered by the shared RAG chain."""

from __future__ import annotations

from src.config.settings import AppSettings
from src.models.chat import ChatResponse, SourceSnippet


class ChatService:
    def __init__(self, settings: AppSettings, vector_store, rag_chain):
        self.settings = settings
        self.vector_store = vector_store
        self.rag_chain = rag_chain

    def ask(self, question: str, session_id: str | None = None) -> ChatResponse:
        resolved_session_id = session_id or self.settings.session.default_session_id
        answer = self.rag_chain.invoke(
            {"input": question},
            self.settings.session_config(resolved_session_id),
        )
        sources = self._search_sources(question)
        return ChatResponse(
            answer=answer,
            session_id=resolved_session_id,
            sources=sources,
        )

    def stream_answer(self, question: str, session_id: str | None = None):
        resolved_session_id = session_id or self.settings.session.default_session_id
        return self.rag_chain.stream(
            {"input": question},
            self.settings.session_config(resolved_session_id),
        )

    def _search_sources(self, question: str) -> list[SourceSnippet]:
        documents = self.vector_store.similarity_search(
            question,
            k=self.settings.rag.retrieval_k,
        )
        return [
            SourceSnippet(content=document.page_content, metadata=document.metadata)
            for document in documents
        ]

