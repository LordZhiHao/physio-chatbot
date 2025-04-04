# # --- START OF FILE frontend.py ---

# import streamlit as st
# # Make sure trilingual_chatbot is in the same directory or Python path
# from trilingual_chatbot import get_response, clear_memories, get_current_language
# import logging # Import logging

# # --- REMOVE set_page_config() FROM HERE ---
# # st.set_page_config(...) # REMOVED

# # --- Custom CSS (Optional, but kept from your original) ---
# # You can keep your existing CSS here if you like the styling
# st.markdown("""
# <style>
#     .chat-message {
#         padding: 1rem;
#         border-radius: 0.5rem;
#         margin-bottom: 0.8rem;
#         display: flex;
#         align-items: flex-start;
#     }
#     .chat-message.user {
#         background-color: #f0f2f6;
#         border-bottom-right-radius: 0.2rem;
#     }
#     .chat-message.bot {
#         background-color: #d1e7dd;
#         border-bottom-left-radius: 0.2rem;
#     }
#     .chat-message .avatar {
#         width: 32px;
#         height: 32px;
#         border-radius: 50%;
#         object-fit: cover;
#         margin-right: 0.8rem;
#     }
#     .chat-message .message {
#         flex-grow: 1;
#     }
#     .stButton button {
#         border-radius: 20px;
#     }
#     .language-indicator {
#         font-size: 0.8rem;
#         color: #6c757d;
#         text-align: right;
#         font-style: italic;
#         margin-bottom: 1rem;
#     }
#     footer {
#         text-align: center;
#         color: gray;
#         padding: 10px;
#         font-size: 0.8rem;
#     }
#     .input-container {
#         display: flex;
#         margin-top: 1rem;
#     }
#     #chat-container {
#         margin-bottom: 5rem;
#     }
#     .stChatMessage {
#         text-align: left; /* Ensure messages align left by default */
#     }
#     .stButton button {
#         border-radius: 20px;
#     }
#     footer {
#         text-align: center;
#         color: gray;
#         padding: 10px;
#         font-size: 0.8rem;
#         position: fixed; /* Keep footer at bottom */
#         bottom: 0;
#         left: 0;
#         width: 100%;
#         background-color: white; /* Add background if needed */
#         z-index: 100;
#     }
#     /* Add some padding to the bottom of the main content area to avoid overlap with footer */
#      .main .block-container {
#         padding-bottom: 5rem;
#     }
#     /* Style for clear button */
#     .clear-chat-button {
#         position: fixed;
#         top: 10px;
#         right: 10px;
#         z-index: 101; /* Ensure it's above other elements */
#     }

# </style>
# """, unsafe_allow_html=True)


# # --- Initialization ---
# st.title("Lo Physiotherapy Assistant 🩺") # This is fine here

# # Initialize chat history in session state if it doesn't exist
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#     # Optional: Add a welcome message
#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": "Hello! 👋 Ask me anything about Lo Physiotherapy's services, treatments, or locations (in English, 中文, or Bahasa Melayu)."
#     })

# # --- Helper Function for Clearing Chat ---
# def clear_chat_history():
#     """Clears chat history in session state and backend memory."""
#     st.session_state.messages = [{
#         "role": "assistant",
#         "content": "Chat history cleared. Ask me anything!"
#     }] # Reset with a message
#     clear_memories() # Clear the backend memory too

# # --- Clear Chat Button ---
# st.markdown("""
#     <div class="clear-chat-button">
#         <!-- The button element itself will be created by st.button below -->
#     </div>
# """, unsafe_allow_html=True)
# if st.button("🗑️ Clear Chat", key="clear_chat_button_main"):
#      clear_chat_history()
#      st.rerun() # Rerun immediately after clearing to reflect the change


# # --- Display Existing Chat Messages ---
# # Iterate through the messages stored in session state
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"]) # Display message content

# # --- Handle User Input ---
# # Use st.chat_input to get user input at the bottom of the page
# if prompt := st.chat_input("How can I help you today?"):
#     # 1. Add user message to session state
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # 2. Display user message immediately
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # 3. Get assistant response
#     with st.chat_message("assistant"):
#         # Show a thinking indicator while waiting
#         with st.spinner("Thinking..."):
#             try:
#                 # Call your backend function from trilingual_chatbot.py
#                 response = get_response(prompt)
#                 # Display the response from the assistant
#                 st.markdown(response)
#             except Exception as e:
#                 # Log the error from the frontend perspective as well
#                 logging.error(f"Frontend caught exception calling get_response: {e}", exc_info=True)
#                 st.error(f"Sorry, I encountered an error trying to respond. Please check the logs or try again later.")
#                 # Ensure response is always a string for appending to state
#                 response = "Error: Could not get a response due to an internal issue."

#     # 4. Add assistant response to session state
#     st.session_state.messages.append({"role": "assistant", "content": response})

#     # Note: Streamlit automatically reruns the script after handling chat_input

# # --- Footer ---
# st.markdown("""
# <footer>
#     Lo Physiotherapy © 2024 | Contact: +6012-529 7825
# </footer>
# """, unsafe_allow_html=True)

# # --- END OF FILE frontend.py ---

# --- START OF FILE frontend.py (MINIMAL TEST) ---
import streamlit as st
import logging
import time

# Ensure logger is configured (it should be by app.py)
logger = logging.getLogger(__name__)
logger.info("--- MINIMAL frontend.py executing ---")

# --- Custom CSS (Optional) ---
# Keep it minimal or remove for testing
st.markdown("""<style> footer { visibility: hidden; } </style>""", unsafe_allow_html=True)

# --- Initialization ---
st.title("Minimal Test App 🧪")

# Initialize chat history if needed
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Minimal app started. Enter any text."})
    logger.info("Initialized session state messages.")

# --- Display Existing Chat Messages ---
logger.info(f"Displaying {len(st.session_state.messages)} messages.")
# Add error handling around message display just in case
try:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
except Exception as e:
    logger.error(f"Error displaying message history: {e}", exc_info=True)
    st.error(f"Error displaying history: {e}")


# --- Handle User Input ---
logger.info("Checking for chat input...")
if prompt := st.chat_input("Enter test message"):
    logger.info(f"Received prompt: '{prompt}'")

    # 1. Add user message to session state
    try:
        st.session_state.messages.append({"role": "user", "content": prompt})
        logger.info("Appended user message to state.")
    except Exception as e:
         logger.error(f"Error appending user message to state: {e}", exc_info=True)
         st.error(f"Error storing user message: {e}")

    # 2. Display user message immediately
    try:
        with st.chat_message("user"):
            st.markdown(prompt)
        logger.info("Displayed user message.")
    except Exception as e:
         logger.error(f"Error displaying user message: {e}", exc_info=True)
         st.error(f"Error showing user message: {e}")

    # 3. Get DUMMY assistant response (NO BACKEND IMPORT/CALL)
    logger.info("Generating simple dummy response...")
    response = f"Minimal echo: '{prompt}'"
    time.sleep(0.1) # Tiny delay simulation

    # 4. Display assistant response
    try:
        with st.chat_message("assistant"):
            st.markdown(response)
        logger.info("Displayed dummy assistant response.")
    except Exception as e:
         logger.error(f"Error displaying assistant message: {e}", exc_info=True)
         st.error(f"Error showing assistant message: {e}")

    # 5. Add assistant response to session state
    try:
        st.session_state.messages.append({"role": "assistant", "content": response})
        logger.info("Appended assistant message to state.")
    except Exception as e:
         logger.error(f"Error appending assistant message to state: {e}", exc_info=True)
         st.error(f"Error storing assistant message: {e}")

else:
    logger.info("No chat input detected this run.")

logger.info("--- MINIMAL frontend.py finished execution for this run ---")

# --- END OF FILE frontend.py (MINIMAL TEST) ---