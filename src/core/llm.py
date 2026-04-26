"""Chat model factory."""

from __future__ import annotations

import os

from langchain_community.chat_models import ChatTongyi

from src.config.settings import AppSettings
from src.utils.exceptions import ConfigurationError


class ChatModelFactory:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    def create(self) -> ChatTongyi:
        if not os.getenv("DASHSCOPE_API_KEY"):
            raise ConfigurationError(
                "Missing DASHSCOPE_API_KEY environment variable."
            )
        return ChatTongyi(model=self.settings.models.chat)

