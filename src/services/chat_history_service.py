"""Persistent file-based chat history storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: Path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.file_path = self.storage_path / self.session_id
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)
        all_messages.extend(messages)
        serialized = [message_to_dict(message) for message in all_messages]
        self.file_path.write_text(
            json.dumps(serialized, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @property
    def messages(self) -> list[BaseMessage]:
        if not self.file_path.exists():
            return []
        raw_messages = json.loads(self.file_path.read_text(encoding="utf-8"))
        return messages_from_dict(raw_messages)

    def clear(self) -> None:
        self.file_path.write_text("[]", encoding="utf-8")


class ChatHistoryFactory:
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def get_history(self, session_id: str) -> FileChatMessageHistory:
        return FileChatMessageHistory(session_id=session_id, storage_path=self.storage_path)

