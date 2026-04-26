"""Legacy compatibility wrapper around the refactored vector store layer."""

from src.bootstrap import get_vector_store
from src.config.settings import get_settings
from src.core.vector_store import ChromaVectorStore


class VectorStoreService:
    def __init__(self, embedding=None):
        if embedding is None:
            self.vector_store = get_vector_store()
        else:
            self.vector_store = ChromaVectorStore(
                settings=get_settings(),
                embedding_function=embedding,
            )

    def get_retriever(self):
        return self.vector_store.get_retriever()
