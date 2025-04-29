# app.py
import streamlit as st

# Set page title
st.set_page_config(page_title="Simple Chat App")

# Streamlit app title
st.title("👋 Hello, Simple Chatbot")

# Text input
user_input = st.text_input("Type something:")

# Display the input back
if user_input:
    st.write("You typed:", user_input)

