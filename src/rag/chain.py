"""RAG chain builder with conversation history."""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory

from src.rag.prompt import build_rag_prompt
from src.rag.retriever import format_documents


class RagChainBuilder:
    def __init__(self, vector_store, chat_model, history_factory):
        self.vector_store = vector_store
        self.chat_model = chat_model
        self.history_factory = history_factory

    def build(self):
        retriever = self.vector_store.get_retriever()
        prompt_template = build_rag_prompt()

        base_chain = (
            {
                "input": RunnableLambda(lambda payload: payload["input"]),
                "history": RunnableLambda(lambda payload: payload["history"]),
                "context": RunnableLambda(lambda payload: payload["input"])
                | retriever
                | RunnableLambda(format_documents),
            }
            | prompt_template
            | self.chat_model
            | StrOutputParser()
        )

        return RunnableWithMessageHistory(
            base_chain,
            self.history_factory,
            input_messages_key="input",
            history_messages_key="history",
        )

