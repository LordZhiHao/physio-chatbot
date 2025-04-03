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
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
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
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex-grow: 1;
    }
    .stTextInput {
        position: fixed;
        bottom: 3rem;
        width: calc(100% - 2rem);
    }
    .language-indicator {
        font-size: 0.8rem;
        color: #6c757d;
        text-align: right;
        padding-right: 1rem;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'current_language' not in st.session_state:
    st.session_state.current_language = "english"

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

# App header
st.title("Lo Physiotherapy Assistant")

# Language detection indicator
language_map = {
    "english": "English",
    "chinese": "中文",
    "malay": "Bahasa Melayu"
}

# Display the language indicator
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712010.png", width=100)
    st.title("Lo Physiotherapy")
    st.markdown("___")
    st.subheader("About")
    st.write("This assistant provides information about Lo Physiotherapy services, treatments, locations, and answers patient questions.")
    st.markdown("___")
    st.subheader("Supported Languages")
    st.write("- English")
    st.write("- Chinese (中文)")
    st.write("- Malay (Bahasa Melayu)")
    st.markdown("___")
    st.write("Current language: ", language_map.get(st.session_state.current_language, "English"))
    
    # Add a button to clear chat history
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    display_message(message["role"], message["content"])

# Chat input
with st.container():
    user_input = st.text_input("Type your message here...", key="user_input", placeholder="How can I help you today?")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message immediately
        display_message("user", user_input)
        
        # Simulate typing with a spinner
        with st.spinner("Thinking..."):
            # Get response from the chatbot
            response = get_response(user_input)
            
            # Check for language changes
            st.session_state.current_language = current_language
            
            # Add a small delay for natural feel
            time.sleep(0.5)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant message
        display_message("assistant", response)
        
        # Clear the input box
        # st.rerun()

# Footer
st.markdown("___")
st.markdown("<div style='text-align: center; color: gray; padding: 10px;'>Lo Physiotherapy © 2025 | Contact: +6012-529 7825</div>", unsafe_allow_html=True)