import streamlit as st
import pandas as pd
from openai import OpenAI

# --- Load dataset ---
df = pd.read_csv("https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv")

# --- Setup OpenRouter / DeepSeek ---
api_key = st.secrets["DEEPSEEK_API_KEY"]
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# --- Streamlit UI ---
st.set_page_config(page_title="Penguin QA Chatbot")
st.title("🐧 Penguin Dataset Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

# --- Display messages ---
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)

# --- User prompt ---
user_input = st.chat_input("Ask something about penguins...")

if user_input:
    st.session_state.history.append(("user", user_input))
    st.chat_message("user").write(user_input)

    # 🧠 Add your dataset as context
    prompt = f"""
You are a data assistant. Here is the Penguin dataset sample:
{df.to_string(index=False)}

Now answer this question using that dataset:
{user_input}
If it's not relevant to the data, just say: "Sorry, I can't answer that based on the dataset."
"""

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "https://vkchatbot.streamlit.app/",
                "X-Title": "VK Chatbot - Penguin QA"
            }
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.chat_message("assistant").write(reply)
    st.session_state.history.append(("assistant", reply))
