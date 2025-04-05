# --- START OF FILE trilingual_chatbot.py ---
import os
import streamlit as st # Keep streamlit import for caching
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory # Keep for now, but see notes
# REMOVED: from langchain.text_splitter import RecursiveCharacterTextSplitter # Not needed for loading
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from datetime import datetime
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from dotenv import load_dotenv
import logging
import time # Optional: for timing debug

# --- Configuration ---
INDEX_LOAD_PATH = "faiss_index"  # Folder where the index is saved
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" # Must match the one used for creation

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Load Environment Variables ---
load_dotenv()

# --- Google API Key Setup ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    st.error("GOOGLE_API_KEY not found in environment variables!")
    raise EnvironmentError("GOOGLE_API_KEY environment variable is required")

# --- REMOVED clinic_info string ---
# The raw text is no longer needed here if loading the index

# --- Cached Function for Vector Store LOADING ---
@st.cache_resource # Decorator to cache the returned object
def load_vector_store():
    """Loads the FAISS vector store from disk, cached for the session."""
    logger.info(f"Attempting to load FAISS index from '{INDEX_LOAD_PATH}' (will run only once per session)...")
    start_time = time.time()

    # Check if index path exists
    if not os.path.isdir(INDEX_LOAD_PATH):
        logger.error(f"FATAL: FAISS index directory not found at '{INDEX_LOAD_PATH}'. Please run create_index.py first.")
        st.error(f"Knowledge base index not found at '{INDEX_LOAD_PATH}'. Cannot start.")
        raise FileNotFoundError(f"FAISS index directory not found: {INDEX_LOAD_PATH}")

    # Check for essential index file (e.g., index.faiss)
    if not os.path.exists(os.path.join(INDEX_LOAD_PATH, "index.faiss")):
         logger.error(f"FATAL: Essential file 'index.faiss' not found in '{INDEX_LOAD_PATH}'. Index may be incomplete or corrupted.")
         st.error(f"Knowledge base index file missing in '{INDEX_LOAD_PATH}'. Cannot start.")
         raise FileNotFoundError(f"Essential file 'index.faiss' missing in {INDEX_LOAD_PATH}")

    try:
        # Load the embeddings model (needed for loading the index)
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}...")
        # Ensure this uses the *exact same* model name as create_index.py
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        logger.info("Embedding model loaded.")

        # Load the FAISS index from disk
        logger.info("Loading FAISS index from disk...")
        vectorstore = FAISS.load_local(
            INDEX_LOAD_PATH,
            embeddings,
            allow_dangerous_deserialization=True # Often needed for loading pickled components
        )
        logger.info("FAISS index loaded successfully from disk.")

        end_time = time.time()
        logger.info(f"Vector store loaded successfully in {end_time - start_time:.2f} seconds.")
        return vectorstore

    except Exception as e:
        logger.error(f"FATAL: Error loading vector database from '{INDEX_LOAD_PATH}': {e}", exc_info=True)
        st.error(f"Failed to load knowledge base: {e}")
        raise # Re-raise to stop app if loading fails

# --- Cached Function for LLM ---
@st.cache_resource # Decorator to cache the returned object
def load_llm():
    """Initializes and returns the LLM, cached for the session."""
    logger.info("Attempting to load LLM (will run only once per session)...")
    start_time = time.time()
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.3,
            api_key=GOOGLE_API_KEY # Pass key directly
        )
        end_time = time.time()
        logger.info(f"LLM loaded successfully in {end_time - start_time:.2f} seconds.")
        return llm
    except Exception as e:
        logger.error(f"FATAL: Failed to initialize LLM: {e}", exc_info=True)
        st.error(f"Failed to initialize AI model: {e}")
        raise # Stop the app if LLM can't load

# --- Initialize by calling cached functions ---
vectorstore = load_vector_store() # Now calls the loading function
llm = load_llm()

# --- Language Detection (remains the same) ---
def detect_language(text):
    if not text or text.strip() == "":
        logger.warning("Empty text provided for language detection")
        return 'english'
    try:
        lang = detect(text)
        if lang in ['zh-cn', 'zh-tw', 'zh']:
            logger.info(f"Detected Chinese language: {lang}")
            return 'chinese'
        elif lang in ['ms', 'id']:
            logger.info(f"Detected Malay language: {lang}")
            return 'malay'
        else:
            logger.info(f"Detected language defaulting to English: {lang}")
            return 'english'
    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e}. Defaulting to English.")
        return 'english'


# --- Prompts (remains the same) ---
english_prompt_template = """
You are a helpful assistant for Lo Physiotherapy clinic in Penang, Malaysia. You provide information about the clinic's services, treatments, locations, and answer common patient questions. However, you are not a medical professional and cannot provide medical advice.

Always be professional, friendly, and helpful. If you don't know the answer to a question, politely say so and suggest contacting the clinic directly at +6012-529 7825.

Chat History:
{chat_history}

Context:
Today's date is {date}. The user is asking about Lo Physiotherapy clinic in Penang, Malaysia. Here's the context retrieved from our available documents:
{context}

Question: {question}

Answer in English:
"""

chinese_prompt_template = """
您好！我是槟城Lo物理治疗诊所的助手。我可以为您提供有关诊所服务、治疗方法、位置以及回答常见问题。

我会始终保持专业、友好和乐于助人的态度。如果我无法回答您的问题，我会礼貌地告诉您，并建议您直接联系诊所，电话：+6012-529 7825。

聊天历史：
{chat_history}

背景信息：
今天是{date}。用户正在询问关于槟城Lo物理治疗诊所的信息。以下是从我们的文档中检索到的相关内容：
{context}

问题：{question}

用中文回答：
"""

malay_prompt_template = """
Anda sedang bercakap dengan pembantu untuk klinik Lo Physiotherapy di Pulau Pinang, Malaysia. Saya menyediakan maklumat tentang perkhidmatan klinik, rawatan, lokasi, dan menjawab soalan-soalan umum pesakit.

Saya akan sentiasa bersikap profesional, mesra, dan membantu. Jika saya tidak tahu jawapan kepada soalan anda, saya akan memberitahu dengan sopan dan mencadangkan anda menghubungi klinik secara langsung di +6012-529 7825.

Sejarah Perbualan:
{chat_history}

Konteks:
Tarikh hari ini ialah {date}. Pengguna sedang bertanya tentang klinik Lo Physiotherapy di Pulau Pinang, Malaysia. Berikut adalah konteks yang diambil dari dokumen kami:
{context}

Soalan: {question}

Jawab dalam Bahasa Melayu:
"""
prompts = {
    'english': PromptTemplate(
        template=english_prompt_template,
        input_variables=["chat_history", "date", "context", "question"]
    ),
    'chinese': PromptTemplate(
        template=chinese_prompt_template,
        input_variables=["chat_history", "date", "context", "question"]
    ),
    'malay': PromptTemplate(
        template=malay_prompt_template,
        input_variables=["chat_history", "date", "context", "question"]
    )
}

# --- Memory Setup (remains the same, still uses module-level memory) ---
memories = {
    'english': ConversationBufferWindowMemory(k=10, return_messages=True),
    'chinese': ConversationBufferWindowMemory(k=10, return_messages=True),
    'malay': ConversationBufferWindowMemory(k=10, return_messages=True)
}
current_language = 'english'

# --- get_response Function (remains largely the same, uses loaded vectorstore/llm) ---
def get_response(query):
    global current_language
    global vectorstore # Access loaded vectorstore
    global llm # Access loaded llm
    global memories

    logger.info(f"--- Starting get_response for query: '{query}' ---")

    if not query or query.strip() == "":
        logger.warning("Empty query received in get_response")
        return "Please ask a question so I can assist you."

    if not vectorstore or not llm:
        logger.error("FATAL: Vectorstore or LLM not available in get_response!")
        st.error("Core components (AI model or knowledge base) are not loaded. Cannot respond.")
        return "I'm sorry, I cannot process your request right now due to an internal setup issue."

    try:
        logger.info("Detecting language...")
        detected_language = detect_language(query)
        current_language = detected_language
        logger.info(f"Language detected: {current_language}")

        today = datetime.now().strftime("%A, %d %B %Y")

        logger.info("Searching vector store...")
        start_search_time = time.time()
        # Ensure similarity_search exists and k is appropriate
        docs = vectorstore.similarity_search(query, k=4)
        context = "\n\n".join([doc.page_content for doc in docs])
        end_search_time = time.time()
        logger.info(f"Vector store search completed in {end_search_time - start_search_time:.2f} seconds. Found {len(docs)} docs.")

        logger.info("Formatting chat history from module memory...")
        chat_history = ""
        try:
             messages = memories[current_language].chat_memory.messages
             for message in messages:
                  if message.type == "human":
                      chat_history += f"User: {message.content}\n"
                  else:
                      chat_history += f"Assistant: {message.content}\n"
             logger.info("Chat history formatted.")
        except Exception as mem_e:
             logger.error(f"Error formatting chat history: {mem_e}", exc_info=True)
             chat_history = "Error retrieving chat history."

        prompt = prompts[current_language]
        logger.info("Creating LLM chain...")
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        logger.info("Running LLM chain...")
        start_llm_time = time.time()
        response = llm_chain.run(
            chat_history=chat_history,
            date=today,
            context=context,
            question=query
        )
        end_llm_time = time.time()
        logger.info(f"LLM chain execution finished in {end_llm_time - start_llm_time:.2f} seconds.")

        try:
            logger.info("Updating module memory...")
            memories[current_language].chat_memory.add_user_message(query)
            memories[current_language].chat_memory.add_ai_message(response)
            logger.info("Module memory updated.")
        except Exception as mem_e:
            logger.error(f"Error updating memory: {mem_e}", exc_info=True)

        logger.info(f"--- Successfully generated response in {current_language} ---")
        return response

    except Exception as e:
        logger.error(f"!!! UNEXPECTED ERROR IN get_response !!!: {e}", exc_info=True)
        st.error("An unexpected error occurred while processing your request.")
        return f"I'm truly sorry, but I encountered an unexpected technical difficulty. Please try asking again in a moment."

# --- Functions to clear memory and get language (remain the same) ---
def clear_memories():
    global memories
    try:
        for lang in memories:
            memories[lang].clear()
        logger.info("All module-level conversation memories cleared")
    except Exception as e:
        logger.error(f"Error clearing memories: {e}", exc_info=True)

def get_current_language():
    global current_language
    return current_language

# --- Local Test Block (remains the same) ---
if __name__ == "__main__":
    print("Lo Physiotherapy Multilingual Assistant (Local Test - Loads Index)")
    print("Supports: English, Chinese (中文), and Malay (Bahasa Melayu)")
    print("="*70)

    # Manually check if index exists for local testing
    if not os.path.isdir(INDEX_LOAD_PATH):
         print(f"\nERROR: Index directory '{INDEX_LOAD_PATH}' not found.")
         print("Please run create_index.py first.")
    else:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() == 'exit':
                break
            # In local test, get_response will use the loaded index
            response = get_response(user_input)
            print(f"\nAssistant: {response}")

# --- END OF FILE trilingual_chatbot.py ---