import streamlit as st
import time
from trilingual_chatbot import get_response, current_language

# Set page configuration
st.set_page_config(
    page_title="Lo Physiotherapy Assistant",
    page_icon="🩺",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #f0f2f6;
        border-bottom-right-radius: 0.2rem;
    }
    .chat-message.bot {
        background-color: #d1e7dd;
        border-bottom-left-radius: 0.2rem;
    }
    .chat-message .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 0.8rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .stButton button {
        border-radius: 20px;
    }
    .language-indicator {
        font-size: 0.8rem;
        color: #6c757d;
        text-align: right;
        font-style: italic;
        margin-bottom: 1rem;
    }
    footer {
        text-align: center;
        color: gray;
        padding: 10px;
        font-size: 0.8rem;
    }
    .input-container {
        display: flex;
        margin-top: 1rem;
    }
    #chat-container {
        margin-bottom: 5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_language' not in st.session_state:
    st.session_state.current_language = "english"
    
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""

# Function to handle message sending
def send_message():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})
        
        # Clear input box
        st.session_state.user_input = ""
        
        # Get response from the chatbot
        with st.spinner(""):
            response = get_response(user_message)
            st.session_state.current_language = current_language
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()

# Function to display chat message
def display_message(role, content):
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user">
            <img class="avatar" src="https://www.iconpacks.net/icons/2/free-user-icon-3296-thumb.png">
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot">
            <img class="avatar" src="https://cdn-icons-png.flaticon.com/512/4712/4712010.png">
            <div class="message">{content}</div>
        </div>
        """, unsafe_allow_html=True)

# Function to clear chat history
def clear_chat():
    st.session_state.messages = []
    st.rerun()

# App header
st.title("Lo Physiotherapy Assistant")

# Language indicator
language_map = {
    "english": "English",
    "chinese": "中文",
    "malay": "Bahasa Melayu"
}

# Show current language
st.markdown(f"""
<div class="language-indicator">
    Currently using: {language_map.get(st.session_state.current_language, "English")}
    &nbsp;&nbsp;
    <span style="cursor: pointer;" onclick="document.getElementById('clear_chat').click()">
        🗑️ Clear chat
    </span>
</div>
""", unsafe_allow_html=True)

# Hidden button for clear chat functionality
st.button("Clear", key="clear_chat", on_click=clear_chat, style="display: none;")

# Display chat container
chat_container = st.container()

# Display chat history in the container
with chat_container:
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; color: #6c757d; margin-top: 4rem; margin-bottom: 4rem;">
            <p>Welcome to Lo Physiotherapy Assistant!</p>
            <p>Ask me anything about our services, treatments, or locations.</p>
            <p style="font-size: 0.8rem;">I can respond in English, Chinese (中文), or Malay (Bahasa Melayu)</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.messages:
            display_message(message["role"], message["content"])

# Input area at the bottom
col1, col2 = st.columns([5, 1])

with col1:
    st.text_input(
        "Type your message here...", 
        key="user_input",
        placeholder="How can I help you today?",
        on_change=send_message if st.session_state.user_input else None
    )

with col2:
    st.button("Send", on_click=send_message)

# Footer
st.markdown("""
<footer>
    Lo Physiotherapy © 2025 | Contact: +6012-529 7825
</footer>
""", unsafe_allow_html=True)