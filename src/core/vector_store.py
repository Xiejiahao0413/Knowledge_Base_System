"""Vector store abstraction backed by Chroma."""

from __future__ import annotations

import os
from typing import Protocol

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.config.settings import AppSettings

os.environ.setdefault("CHROMA_TELEMETRY", "false")


class VectorStoreProtocol(Protocol):
    def add_texts(self, texts: list[str], metadatas: list[dict]) -> list[str]:
        """Persist texts into the underlying vector store."""

    def get_retriever(self):
        """Return a LangChain retriever."""

    def similarity_search(self, query: str, k: int) -> list[Document]:
        """Run a similarity search."""

    def count(self) -> int:
        """Return stored document count."""


class ChromaVectorStore:
    def __init__(self, settings: AppSettings, embedding_function):
        self.settings = settings
        self.settings.chroma_db_path.mkdir(parents=True, exist_ok=True)
        self._client = Chroma(
            collection_name=self.settings.rag.collection_name,
            embedding_function=embedding_function,
            persist_directory=str(self.settings.chroma_db_path),
        )

    def add_texts(self, texts: list[str], metadatas: list[dict]) -> list[str]:
        return self._client.add_texts(texts=texts, metadatas=metadatas)

    def get_retriever(self):
        return self._client.as_retriever(
            search_kwargs={"k": self.settings.rag.retrieval_k}
        )

    def similarity_search(self, query: str, k: int | None = None) -> list[Document]:
        return self._client.similarity_search(
            query,
            k=k or self.settings.rag.retrieval_k,
        )

    def count(self) -> int:
        return self._client._collection.count()

