import streamlit as st
from main_2 import generate_answer  # ✅ RAG logic here

# --- App Setup ---
st.set_page_config(page_title="HackBuddy - Your Project Wingman", )
st.title("HackBuddy")
st.subheader("Your AI teammate for hackathons, datasets, and projects")

# --- Intro Message ---
st.info(
    "Hello! Welcome to **HackBuddy**! \n\n"
    "I’m here to help you:\n"
    "- Discover project ideas for hackathons\n"
    "- Find the perfect dataset\n"
    "- Explore GitHub repositories\n\n"
    "Try asking things like:\n"
    "• _Dataset for crop disease detection_\n"
    "• _Ideas for a mental health app_\n"
    "• _Top GitHub repos for time series forecasting_"
)

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Input Box ---
user_input = st.chat_input("Ask me anything about projects, datasets, GitHub...")
if user_input:
    with st.spinner("Thinking..."):
        response = generate_answer(user_input)
    st.session_state.chat_history.append((user_input, response))

# --- Chat Display (Top to Bottom) ---
for user_query, bot_response in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(user_query)
    with st.chat_message("assistant"):
        st.markdown(bot_response)
