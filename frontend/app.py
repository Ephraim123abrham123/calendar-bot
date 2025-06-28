import streamlit as st
import requests

st.title("📅 AI Calendar Assistant")

if 'messages' not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"message": user_input}
        ).json()
        reply = response.get("reply", "Sorry, I didn't understand")
    except:
        reply = "⚠️ Backend not running! Run: uvicorn backend.main:app --reload"
    
    st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])