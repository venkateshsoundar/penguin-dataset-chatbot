# Penguin Dataset Chatbot

An interactive Streamlit application that allows users to explore the Palmer Penguins dataset via conversational queries. Powered by OpenRouter AI (DeepSeek) for context-aware answers.

---

## 🔧 Features

- **Chat Interface**: Built using Streamlit's `st.chat_input` and `st.chat_message`.
- **Data Context**: Loads the cleaned Palmer Penguins dataset for dynamic prompt inclusion.
- **AI Backend**: Utilizes OpenRouter AI (DeepSeek) via the `openai.OpenAI` client.
- **Session Memory**: Maintains full conversation history across queries.

---

## 📂 Repository Structure

```
.
├── .devcontainer/             # VS Code Codespaces configuration
├── .streamlit/                # Streamlit settings & secrets
│   └── secrets.toml           # Store DEEPSEEK_API_KEY
├── streamlit_app.py           # Main application script
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Setup & Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/venkateshsoundar/vk_chatbot.git
   cd vk_chatbot
   ```

2. **Create & activate** a virtual environment  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**  
   Add your DeepSeek API key to `.streamlit/secrets.toml`:
   ```toml
   DEEPSEEK_API_KEY = "your_openrouter_or_deepseek_api_key_here"
   ```

---

## ▶️ Running the App

```bash
streamlit run streamlit_app.py
```
Open the displayed URL (e.g., `http://localhost:8501`) in your browser and start chatting!

---

## ✨ Usage Example

- Ask about species characteristics: 
  > “What is the average bill length of Adelie penguins?”
- Compare groups:
  > “How do Gentoo and Chinstrap penguins differ in flipper length?”

---

## 🤝 Contributing

1. Fork this repository  
2. Create a feature branch: `git checkout -b feature/YourFeature`  
3. Commit changes: `git commit -m "Add feature"`  
4. Push & open a Pull Request

---

## 📜 License

MIT License © 2025 Venkateshwaran B. S.
