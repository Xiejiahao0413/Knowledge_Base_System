"""Legacy compatibility wrapper for file-based chat history."""

from src.bootstrap import get_history_factory
from src.services.chat_history_service import FileChatMessageHistory


def get_history(session_id: str) -> FileChatMessageHistory:
    return get_history_factory().get_history(session_id)
