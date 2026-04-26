"""Embedding model factory."""

from __future__ import annotations

import os

from langchain_community.embeddings import DashScopeEmbeddings

from src.config.settings import AppSettings
from src.utils.exceptions import ConfigurationError


class EmbeddingFactory:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    def create(self) -> DashScopeEmbeddings:
        if not os.getenv("DASHSCOPE_API_KEY"):
            raise ConfigurationError(
                "Missing DASHSCOPE_API_KEY environment variable."
            )
        return DashScopeEmbeddings(model=self.settings.models.embedding)

