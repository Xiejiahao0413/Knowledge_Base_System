"""Prompt templates for grounded QA."""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def build_rag_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是企业知识库问答助手。请优先依据参考资料作答，回答要简洁、专业、可执行。"
                "如果参考资料不足，请明确说明信息不足，不要编造。\n\n参考资料：\n{context}",
            ),
            MessagesPlaceholder("history"),
            ("user", "{input}"),
        ]
    )

