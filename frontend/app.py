import streamlit as st
import requests
import time
from backend.agent import build_agent  # Correct absolute import

# Initialize the agent
agent = build_agent()

# App Configuration
st.set_page_config(
    page_title="📅 AI Calendar Assistant",
    page_icon="📅",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stChatInput { bottom: 2rem; }
    .stChatMessage { padding: 1rem; }
    .error { color: #ff4b4b; }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can help schedule meetings. Try saying 'Book a meeting tomorrow at 2pm'"}
    ]

# UI Elements
st.title("📅 AI Calendar Assistant")
with st.sidebar:
    st.header("Settings")
    use_backend = st.toggle("Use FastAPI Backend", True)
    backend_url = st.text_input(
        "Backend URL", 
        value="http://localhost:8000",
        disabled=not use_backend
    )

# Chat Display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input Handling
if user_input := st.chat_input("Type your request..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        status_text = st.empty()
        status_text.markdown("▌")  # Typing indicator
        
        try:
            if use_backend:
                # FastAPI backend mode
                response = requests.post(
                    f"{backend_url}/chat",
                    json={"message": user_input},
                    timeout=10
                )
                reply = response.json().get("reply", "Sorry, I didn't understand")
            else:
                # Direct LangGraph agent mode
                result = agent.invoke({"user_input": user_input})
                reply = result.get("response", "No response from agent")
                
        except Exception as e:
            reply = f"""<span class="error">⚠️ Error: {str(e)}</span>
            
            **Troubleshooting:**
            - { "Backend not running? Try:\n```bash\nuvicorn backend.main:app --reload\n```" if use_backend else "Agent failed to process request"}
            """
            st.markdown(reply, unsafe_allow_html=True)
        
        # Typewriter effect
        full_reply = ""
        for chunk in reply.split(" "):
            full_reply += chunk + " "
            status_text.markdown(full_reply + "▌")
            time.sleep(0.05)
        
        status_text.markdown(full_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": reply})