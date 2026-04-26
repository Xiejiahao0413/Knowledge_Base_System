"""Unified Streamlit application."""

from __future__ import annotations

import streamlit as st

from src.web.pages.chat import render_chat_page
from src.web.pages.upload import render_upload_page


def main() -> None:
    st.set_page_config(page_title="知识库系统", page_icon="🧠", layout="wide")
    page = st.sidebar.radio("功能导航", ["知识库上传", "知识库问答"])
    if page == "知识库上传":
        render_upload_page()
        return
    render_chat_page()


if __name__ == "__main__":
    main()
