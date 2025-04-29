import streamlit as st
from openai import OpenAI

# -----------------------------
# STREAMLIT CONFIGURATION
# -----------------------------
st.set_page_config(page_title="VK Chatbot", layout="wide")
st.title("🤖 VK Chatbot - Powered by DeepSeek-R1")

# -----------------------------
# LOAD API KEY SECURELY
# -----------------------------
api_key = st.secrets["DEEPSEEK_API_KEY"]
st.text(f"✅ Loaded key: {api_key[:6]}**********")  # Only print prefix

# -----------------------------
# SETUP OPENROUTER CLIENT
# -----------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# -----------------------------
# SESSION STATE FOR CHAT
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show all previous messages
for role, message in st.session_state.messages:
    st.chat_message(role).write(message)

# -----------------------------
# CHAT INPUT
# -----------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message and store it
    st.chat_message("user").write(user_input)
    st.session_state.messages.append(("user", user_input))

    # Build the message history for the model
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *[
                    {"role": role, "content": content}
                    for role, content in st.session_state.messages
                ],
            ],
            extra_headers={
                "HTTP-Referer": "https://vkchatbot.streamlit.app/",
                "X-Title": "VK Chatbot with DeepSeek"
            }
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {e}"

    # Show assistant reply and store it
    st.chat_message("assistant").write(reply)
    st.session_state.messages.append(("assistant", reply))
