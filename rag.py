"""Legacy compatibility wrapper around the refactored chat service."""

from src.bootstrap import get_chat_service


class _LegacyChainAdapter:
    def __init__(self, chat_service):
        self.chat_service = chat_service

    def stream(self, payload: dict, config: dict | None = None):
        session_id = _extract_session_id(config)
        return self.chat_service.stream_answer(payload["input"], session_id=session_id)

    def invoke(self, payload: dict, config: dict | None = None):
        session_id = _extract_session_id(config)
        response = self.chat_service.ask(payload["input"], session_id=session_id)
        return response.answer


def _extract_session_id(config: dict | None) -> str | None:
    if not config:
        return None
    configurable = config.get("configurable", {})
    return configurable.get("session_id")


class RagService:
    def __init__(self):
        self.chat_service = get_chat_service()
        self.chain = _LegacyChainAdapter(self.chat_service)

    def ask(self, question: str, session_id: str | None = None):
        return self.chat_service.ask(question=question, session_id=session_id)
