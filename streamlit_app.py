# app.py
import streamlit as st

# Setup page
st.set_page_config(page_title="Simple Chatbot")

st.title("🤖 My Simple Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all previous messages
for role, msg in st.session_state.messages:
    st.chat_message(role).write(msg)

# Chat input
user_input = st.chat_input("Say something...")

# Store and reply
if user_input:
    st.session_state.messages.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # Simple hardcoded bot response
    bot_reply = f"Echo: {user_input}"
    st.session_state.messages.append(("assistant", bot_reply))
    st.chat_message("assistant").write(bot_reply)
