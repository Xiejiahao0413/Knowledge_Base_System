"""Chat Streamlit page."""

from __future__ import annotations

import streamlit as st

from src.bootstrap import get_chat_service, get_knowledge_service
from src.config.settings import get_settings
from src.utils.exceptions import KnowledgeBaseSystemError
from src.web.components.sidebar import render_sidebar


def render_chat_page() -> None:
    settings = get_settings()
    st.title("知识库问答")
    st.caption("结合知识库检索结果和对话历史回答问题。")

    session_id = st.sidebar.text_input(
        "会话 ID",
        value=st.session_state.get("session_id", settings.session.default_session_id),
    )
    st.session_state["session_id"] = session_id

    try:
        render_sidebar(settings, get_knowledge_service().get_stats())
    except KnowledgeBaseSystemError as error:
        render_sidebar(settings)
        st.warning(f"知识库服务尚未就绪：{error}")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "你好，我已经准备好基于知识库回答问题。"}
        ]

    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).write(message["content"])

    prompt = st.chat_input("请输入你的问题")
    if not prompt:
        return

    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    chunks: list[str] = []
    try:
        with st.chat_message("assistant"):
            stream = get_chat_service().stream_answer(prompt, session_id=session_id)

            def capture():
                for chunk in stream:
                    chunks.append(chunk)
                    yield chunk

            st.write_stream(capture())
    except KnowledgeBaseSystemError as error:
        error_message = str(error)
        st.error(error_message)
        st.session_state["messages"].append({"role": "assistant", "content": error_message})
        return

    answer = "".join(chunks)
    st.session_state["messages"].append({"role": "assistant", "content": answer})
