"""Application dependency container."""

from __future__ import annotations

from functools import lru_cache

from src.config.logging_config import configure_logging
from src.config.settings import AppSettings, get_settings
from src.core.embeddings import EmbeddingFactory
from src.core.llm import ChatModelFactory
from src.core.vector_store import ChromaVectorStore
from src.rag.chain import RagChainBuilder
from src.services.chat_history_service import ChatHistoryFactory
from src.services.chat_service import ChatService
from src.services.document_service import DocumentService
from src.services.knowledge_service import KnowledgeService


@lru_cache(maxsize=1)
def _configured_settings() -> AppSettings:
    settings = get_settings()
    configure_logging(settings)
    return settings


@lru_cache(maxsize=1)
def get_document_service() -> DocumentService:
    return DocumentService()


@lru_cache(maxsize=1)
def get_history_factory() -> ChatHistoryFactory:
    settings = _configured_settings()
    return ChatHistoryFactory(settings.chat_history_path)


@lru_cache(maxsize=1)
def get_vector_store():
    settings = _configured_settings()
    embedding_model = EmbeddingFactory(settings).create()
    return ChromaVectorStore(settings=settings, embedding_function=embedding_model)


@lru_cache(maxsize=1)
def get_knowledge_service() -> KnowledgeService:
    settings = _configured_settings()
    return KnowledgeService(settings=settings, vector_store=get_vector_store())


@lru_cache(maxsize=1)
def get_chat_service() -> ChatService:
    settings = _configured_settings()
    rag_chain = RagChainBuilder(
        vector_store=get_vector_store(),
        chat_model=ChatModelFactory(settings).create(),
        history_factory=get_history_factory().get_history,
    ).build()
    return ChatService(
        settings=settings,
        vector_store=get_vector_store(),
        rag_chain=rag_chain,
    )
