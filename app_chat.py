import streamlit as st

from src.web.pages.chat import render_chat_page


if __name__ == "__main__":
    st.set_page_config(page_title="知识库问答", page_icon="💬", layout="wide")
    render_chat_page()
