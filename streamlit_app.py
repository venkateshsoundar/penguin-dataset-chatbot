import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from openai import OpenAI

# 1) Use a wide layout
st.set_page_config(layout="wide")

# 2) Split into main & chat columns
col_main, col_chat = st.columns([3, 1])

# --- MAIN COLUMN ---
with col_main:
    st.title('🐧 Penguin Dataset Explorer')
    st.write('This app builds a RandomForest model on the Palmer Penguins dataset and lets you explore data, visualize it, and see predictions.')

    # Load data
    df = pd.read_csv(
        "https://raw.githubusercontent.com/dataprofessor/data/refs/heads/master/penguins_cleaned.csv"
    )

    # Raw data & visuals
    with st.expander('🔍 Data Preview & Visuals', expanded=True):
        st.write("**Raw Data**")
        st.dataframe(df, use_container_width=True)
        st.write("**Scatter:** bill_length_mm vs body_mass_g")
        st.scatter_chart(df, x="bill_length_mm", y="body_mass_g", color="species")

    # Sidebar-style inputs (but placed here so they’re part of main layout)
    with st.expander('⚙️ Input Features'):
        island = st.selectbox("Island", df["island"].unique())    
        bill_length_mm = st.slider(
            'Bill length (mm)',
            float(df['bill_length_mm'].min()),
            float(df['bill_length_mm'].max()),
            float(df['bill_length_mm'].mean())
        )
        bill_depth_mm = st.slider(
            'Bill depth (mm)',
            float(df['bill_depth_mm'].min()),
            float(df['bill_depth_mm'].max()),
            float(df['bill_depth_mm'].mean())
        )
        flipper_length_mm = st.slider(
            'Flipper length (mm)',
            float(df['flipper_length_mm'].min()),
            float(df['flipper_length_mm'].max()),
            float(df['flipper_length_mm'].mean())
        )
        body_mass_g = st.slider(
            'Body mass (g)',
            float(df['body_mass_g'].min()),
            float(df['body_mass_g'].max()),
            float(df['body_mass_g'].mean())
        )
        sex = st.selectbox("Sex", df["sex"].unique())

        # Build the input DataFrame
        user_data = {
            'island': island,
            'bill_length_mm': bill_length_mm,
            'bill_depth_mm': bill_depth_mm,
            'flipper_length_mm': flipper_length_mm,
            'body_mass_g': body_mass_g,
            'sex': sex
        }
        input_df = pd.DataFrame(user_data, index=[0])
        combined = pd.concat([input_df, df.drop('species', axis=1)], ignore_index=True)

    # Encoding & modelling
    with st.expander('🛠️ Data Prep & Prediction', expanded=True):
        # One-hot encode
        encode_cols = ['island', 'sex']
        encoded = pd.get_dummies(combined, columns=encode_cols, prefix=encode_cols)
        X = encoded.iloc[1:, :]   # all except first
        input_row = encoded.iloc[[0]]

        # Encode target
        mapper = {'Adelie':0,'Chinstrap':1,'Gentoo':2}
        y = df['species'].map(mapper)

        # Train & predict
        clf = RandomForestClassifier()
        clf.fit(X, y)
        proba = clf.predict_proba(input_row)[0]
        proba_df = pd.DataFrame([proba], columns=['Adelie','Chinstrap','Gentoo'])

        st.write("**Prediction probabilities**")
        st.dataframe(proba_df, use_container_width=True)

        species = np.array(['Adelie','Chinstrap','Gentoo'])
        st.success(f"Predicted species: {species[np.argmax(proba)]}", icon="👍")


# --- CHAT COLUMN ---
with col_chat:
    st.header("💬 Penguin ChatBot")
    # Initialize OpenRouter client
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Persist history
    if "history" not in st.session_state:
        st.session_state.history = []

    # Display past chat
    for role, msg in st.session_state.history:
        st.chat_message(role).write(msg)

    # New user input
    user_input = st.chat_input("Ask something about penguins…")
    if user_input:
        st.session_state.history.append(("user", user_input))
        st.chat_message("user").write(user_input)

        # Build prompt with dataset context
        prompt = f"""
You are a data assistant. Here is a sample of the Penguin dataset:
{df.head.to_string(index=False)}

Answer the user’s question based only on this data:
{user_input}

If irrelevant, say: "Sorry, I can't answer that based on the dataset."
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

        st.session_state.history.append(("assistant", reply))
        st.chat_message("assistant").write(reply)
