# app_streamlit.py
import os
import streamlit as st
from bot_core import Chatbot

st.set_page_config(page_title="PyPI & Python FAQ Chatbot", page_icon="🐍")

@st.cache_resource
def load_bot():
    # base_dir = folder where THIS file lives
    base_dir = os.path.dirname(__file__)
    return Chatbot(base_dir=base_dir)

bot = load_bot()

st.title("🐍 PyPI & Python FAQ Chatbot")
st.caption("Type a package name / pip command, or ask a Python FAQ question.")

# simple chat UI
if "history" not in st.session_state:
    st.session_state.history = []

for role, text in st.session_state.history:
    with st.chat_message(role):
        st.markdown(text)

prompt = st.chat_input("Ask me something…")
if prompt:
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    answer = bot.get_answer(prompt)
    st.session_state.history.append(("assistant", answer))
    with st.chat_message("assistant"):
        st.markdown(answer)

