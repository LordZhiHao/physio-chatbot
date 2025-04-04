# import os
# from langchain.chains import LLMChain
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.memory import ConversationBufferWindowMemory
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.prompts import PromptTemplate
# from datetime import datetime
# from langdetect import detect
# from langdetect.lang_detect_exception import LangDetectException
# from dotenv import load_dotenv
# import logging

# # Set up logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# # Set up Google API key
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# if not GOOGLE_API_KEY:
#     logger.error("GOOGLE_API_KEY not found in environment variables")
#     raise EnvironmentError("GOOGLE_API_KEY environment variable is required")
# os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# # Load clinic information
# clinic_info = """
# **About Lo Physiotherapy:**

# Lo Physiotherapy began its journey in 1996 with a mission to provide professional and effective pain management solutions that are both affordable and accessible to the community. With 28 years of experience, over 400,000 patient visits, and 6 branches across Penang, their commitment remains strong. They address the growing challenge of back pain, which affects 8 out of 10 people globally, by offering precise diagnostic services, effective treatments, and patient education for sustainable lifestyle habits. Lo Physiotherapy believes everyone deserves a healthy and fulfilling life and strives to make a difference daily, one patient at a time.

# **Our Physiotherapy Philosophy (H.E.A.R.T.S):**

# At Lo Physiotherapy, the patient is at the heart of everything they do. Their philosophy is built on the acronym H.E.A.R.T.S, which stands for:

# *   Healing: Focusing on the patient's overall well-being and recovery.
# *   Evidence: Utilizing evidence-based practices, combining scientific research with clinical experience to tailor effective treatment plans.
# *   Accurate Diagnosis: Laying the foundation for a healing journey by identifying the underlying cause of discomfort through comprehensive assessments.
# *   Relationships: Building long-term connections and partnerships with patients, adapting to their evolving needs.
# *   Teamwork: Collaborating for increased accountability, pooling expertise to ensure no aspect of health is overlooked.
# *   Sustainability: Empowering patients with knowledge and habits for lasting health benefits, promoting long-term well-being.

# **Conditions Treated:**

# Lo Physiotherapy specializes in treating a wide range of conditions, including:

# *   Neck Pain & Headache
# *   Shoulder, Elbow & Arm Pain
# *   Back Pain
# *   Sciatica
# *   Slipped Disc
# *   Knee Pain
# *   Plantar Fasciitis, Ankle & Foot Pain

# **Treatment Approaches:**

# Lo Physiotherapy provides evidence-based physiotherapy, offering various treatment methods tailored to individual needs:

# *   Spinal Instrument Adjustment: Enhances spinal alignment, joint mobility, and nerve function.
# *   Manual Therapy: Hands-on techniques to alleviate pain and restore function in the musculoskeletal system.
# *   Medical Acupuncture: Science-based acupuncture targeting specific conditions, relieving pain, and promoting recovery.
# *   Dry Needling: Targets tight muscle areas (trigger points) to ease muscle tension and pain.
# *   Exercise Therapy: Customized physical activities to improve health and address specific conditions.
# *   Shockwave Therapy: Uses sound waves to accelerate the body's healing in tendons, ligaments, and soft tissues.
# *   Interferential Therapy: Employs medium-frequency electrical stimulation to treat pain, diminish inflammation, and encourage recovery.
# *   Ultrasound Therapy: Promotes healing, eases pain, and enhances mobility in musculoskeletal issues.
# *   Traction Therapy: Eases pressure on discs and nerves by gently stretching joints, especially in the spine.
# *   Parkinson Rehabilitation: Customised program to address both motor and non-motor symptoms, minimizing symptoms and enhancing life quality

# **Symptoms Addressed and Treatment Approaches:**

# *   **Stiff & painful muscles:** Lo Physiotherapy uses manual therapy, dry needling, and exercise therapy to release muscle tension, reduce pain, and improve mobility.
# *   **Pain from work or workouts:** Treatment plans are tailored to address the specific causes of pain, often involving manual therapy, exercise therapy, and modalities like ultrasound or interferential therapy to promote healing and reduce inflammation.
# *   **Neck pain from sitting too much:** Spinal instrument adjustment, manual therapy, and exercise therapy are used to correct posture, improve spinal alignment, and alleviate neck pain.
# *   **Backache from prolonged sitting, standing, and working:** Treatment focuses on spinal decompression, manual therapy, and core strengthening exercises to reduce pressure on the spine and improve back support.
# *   **Numbness on your arm and leg:** Neural mobilization techniques, manual therapy, and spinal adjustments are used to address nerve compression and improve nerve function.
# *   **Shoulder pain in your daily activity:** Shoulder joint instrument adjustment, manual therapy, and targeted exercises are used to improve shoulder mobility, reduce pain, and restore function.
# *   **Knee pain at early morning, raise from prolong siting and up or down stair cases:** Knee joint instrument adjustment, manual therapy, and strengthening exercises are used to improve knee alignment, reduce pain, and enhance mobility.
# *   **Heel pain at early morning wake up, raise from prolong sitting and walking:** Manual therapy, dry needling, custom-made orthotics/insoles, and specific exercises are used to address plantar fasciitis, reduce pain, and improve foot biomechanics.

# **Locations and Contact Information:**

# *   **Lo Physiotherapy Tanjong Tokong branch:** [Location] C-1-6 Vantage (Level 1), Jalan Desiran Tanjong, 10470 Tanjong Tokong, Penang. [Opening Hours] Mon - Thurs: 9.30am - 9pm, Fri: 9.30am - 6pm, Sat: 8.30am - 5pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 016-9341230, 012-5297825.
# *   **Lo Physiotherapy Georgetown Specialist Hospital branch:** [Location] 2A, Jalan Masjid Negeri, 11900, Georgetown, Penang. [Opening Hours] Mon & Thurs: 9.30am - 8pm, Tue & Wed: 9.30am - 6pm, Fri: 9.30am - 5pm, Sat: 8.30am - 5pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 017-9123081.
# *   **Lo Physiotherapy Kek Lok Si Charitable Hospital branch:** [Location] 623, Jalan Balik Pulau, Penang Ayer Itam, 11500 Ayer Itam, Penang. [Opening Hours] Mon & Thurs: 9.30am - 8pm, Tue & Wed: 9.30am - 6pm, Fri: 9.30am - 5pm, Sat: 8.30am - 1pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 016-5293996.
# *   **Lo Physiotherapy Raja Uda branch:** [Location] Block A-79, Jalan Raja Uda, Pusat Perniagaan Raja Uda, 12300 Butterworth, Penang. [Opening Hours] Mon, Wed & Thurs: 9.30am - 8.30pm, Tue & Fri: 9.30am - 6pm, Sat: 9am - 5pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 016-8869934.
# *   **Oh Physiotherapy Bayan Lepas branch:** [Location] 1-2-20 Kompleks I-Avenue, Bukit Jambul, Bayan Lepas, Penang. [Opening Hours] Mon & Wed: 9.30am - 8pm, Tue & Thurs: 9.30am - 7pm, Fri: 9.30am - 6pm, Sat: 8.30am - 4pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 04-6410850.
# *   **Oh Physiotherapy B BRAUN Factory branch:** [Location] Bayan Lepas Industrial Park, 10810 Bayan Baru, Penang. [Opening Hours] BY APPOINTMENT ONLY. Tue & Wed: 2pm - 4pm, Thurs: 9.30am - 12pm. Tel: 016-4337780.

# **Contact Information:**

# *   Phone: +6012-529 7825
# """

# # Set up vector database
# def create_vectordb():
#     """Create and return a vector database from the clinic information."""
#     try:
#         # Split the text into chunks
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=1000,
#             chunk_overlap=200,
#             length_function=len,
#         )
#         chunks = text_splitter.split_text(clinic_info)
        
#         # Create embeddings and vector store
#         embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#         vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        
#         logger.info("Vector database created successfully")
#         return vectorstore
#     except Exception as e:
#         logger.error(f"Error creating vector database: {e}")
#         raise

# # Initialize vector database
# vectorstore = create_vectordb()

# # Define language detection function with improved error handling
# def detect_language(text):
#     """Detect the language of the input text with better error handling."""
#     if not text or text.strip() == "":
#         logger.warning("Empty text provided for language detection")
#         return 'english'
    
#     try:
#         lang = detect(text)
#         # Map language codes to our supported languages
#         if lang in ['zh-cn', 'zh-tw', 'zh']:
#             logger.info(f"Detected Chinese language: {lang}")
#             return 'chinese'
#         elif lang in ['ms', 'id']:  # Indonesian is similar to Malay
#             logger.info(f"Detected Malay language: {lang}")
#             return 'malay'
#         else:
#             logger.info(f"Detected language defaulting to English: {lang}")
#             return 'english'  # Default to English for other languages
#     except LangDetectException as e:
#         logger.warning(f"Language detection failed: {e}. Defaulting to English.")
#         return 'english'  # Default to English if detection fails

# # Define prompts for each language
# english_prompt_template = """
# You are a helpful assistant for Lo Physiotherapy clinic in Penang, Malaysia. You provide information about the clinic's services, treatments, locations, and answer common patient questions. However, you are not a medical professional and cannot provide medical advice.

# Always be professional, friendly, and helpful. If you don't know the answer to a question, politely say so and suggest contacting the clinic directly at +6012-529 7825.

# Chat History:
# {chat_history}

# Context:
# Today's date is {date}. The user is asking about Lo Physiotherapy clinic in Penang, Malaysia. Here's the context retrieved from our available documents:
# {context}

# Question: {question}

# Answer in English:
# """

# chinese_prompt_template = """
# 您好！我是槟城Lo物理治疗诊所的助手。我可以为您提供有关诊所服务、治疗方法、位置以及回答常见问题。

# 我会始终保持专业、友好和乐于助人的态度。如果我无法回答您的问题，我会礼貌地告诉您，并建议您直接联系诊所，电话：+6012-529 7825。

# 聊天历史：
# {chat_history}

# 背景信息：
# 今天是{date}。用户正在询问关于槟城Lo物理治疗诊所的信息。以下是从我们的文档中检索到的相关内容：
# {context}

# 问题：{question}

# 用中文回答：
# """

# malay_prompt_template = """
# Anda sedang bercakap dengan pembantu untuk klinik Lo Physiotherapy di Pulau Pinang, Malaysia. Saya menyediakan maklumat tentang perkhidmatan klinik, rawatan, lokasi, dan menjawab soalan-soalan umum pesakit.

# Saya akan sentiasa bersikap profesional, mesra, dan membantu. Jika saya tidak tahu jawapan kepada soalan anda, saya akan memberitahu dengan sopan dan mencadangkan anda menghubungi klinik secara langsung di +6012-529 7825.

# Sejarah Perbualan:
# {chat_history}

# Konteks:
# Tarikh hari ini ialah {date}. Pengguna sedang bertanya tentang klinik Lo Physiotherapy di Pulau Pinang, Malaysia. Berikut adalah konteks yang diambil dari dokumen kami:
# {context}

# Soalan: {question}

# Jawab dalam Bahasa Melayu:
# """

# # Create a dictionary to store the prompts
# prompts = {
#     'english': PromptTemplate(
#         template=english_prompt_template,
#         input_variables=["chat_history", "date", "context", "question"]
#     ),
#     'chinese': PromptTemplate(
#         template=chinese_prompt_template,
#         input_variables=["chat_history", "date", "context", "question"]
#     ),
#     'malay': PromptTemplate(
#         template=malay_prompt_template,
#         input_variables=["chat_history", "date", "context", "question"]
#     )
# }

# # Set up the LLM
# def get_llm():
#     """Initialize and return the LLM with appropriate settings."""
#     try:
#         return ChatGoogleGenerativeAI(
#             model="gemini-1.5-flash", 
#             temperature=0.3, 
#             api_key=os.getenv("GOOGLE_API_KEY")
#         )
#     except Exception as e:
#         logger.error(f"Failed to initialize LLM: {e}")
#         raise

# # Initialize LLM
# llm = get_llm()

# # Set up memory - we'll use separate memories for each language
# # Using WindowMemory to keep conversation context manageable
# memories = {
#     'english': ConversationBufferWindowMemory(k=10, return_messages=True),
#     'chinese': ConversationBufferWindowMemory(k=10, return_messages=True),
#     'malay': ConversationBufferWindowMemory(k=10, return_messages=True)
# }

# # Current language tracker - module-level variable
# current_language = 'english'  # Default language

# def get_response(query):
#     """Get a response from the chatbot in the appropriate language."""
#     global current_language
    
#     if not query or query.strip() == "":
#         logger.warning("Empty query received")
#         return "Please ask a question so I can assist you."
    
#     try:
#         # Detect language of the query
#         detected_language = detect_language(query)
#         current_language = detected_language
        
#         today = datetime.now().strftime("%A, %d %B %Y")
        
#         # Get relevant documents with error handling
#         try:
#             docs = vectorstore.similarity_search(query, k=4)
#             # Format the context from documents
#             context = "\n\n".join([doc.page_content for doc in docs])
#         except Exception as e:
#             logger.error(f"Error retrieving documents: {e}")
#             context = "Error retrieving relevant information. Using general knowledge."
        
#         # Format chat history
#         chat_history = ""
#         messages = memories[current_language].chat_memory.messages
#         for message in messages:
#             if message.type == "human":
#                 chat_history += f"User: {message.content}\n"
#             else:
#                 chat_history += f"Assistant: {message.content}\n"
        
#         # Get the appropriate prompt for the detected language
#         prompt = prompts[current_language]
        
#         # Create the LLM chain
#         llm_chain = LLMChain(llm=llm, prompt=prompt)
        
#         # Get the response
#         response = llm_chain.run(
#             chat_history=chat_history,
#             date=today,
#             context=context,
#             question=query
#         )
        
#         # Update memory for the current language
#         memories[current_language].chat_memory.add_user_message(query)
#         memories[current_language].chat_memory.add_ai_message(response)
        
#         logger.info(f"Generated response in {current_language}")
#         return response
    
#     except Exception as e:
#         logger.error(f"Error generating response: {e}")
#         return f"I'm sorry, but I encountered an error while processing your request. Please try again or contact the clinic directly at +6012-529 7825."

# # Function to clear memory for all languages
# def clear_memories():
#     """Clear conversation memory for all languages"""
#     for lang in memories:
#         memories[lang].clear()
#     logger.info("All conversation memories cleared")
    
# # Function to get current language
# def get_current_language():
#     """Return the current language being used"""
#     return current_language

# # Test the chatbot
# if __name__ == "__main__":
#     print("Lo Physiotherapy Multilingual Assistant (Type 'exit' to quit)")
#     print("Supports: English, Chinese (中文), and Malay (Bahasa Melayu)")
#     print("="*70)
    
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() == 'exit':
#             break

#         response = get_response(user_input)
#         print(f"\nAssistant: {response}")


import os
# ---- ADD STREAMLIT IMPORT ----
import streamlit as st
# -----------------------------
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory # Keep for now, but see notes
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from datetime import datetime
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from dotenv import load_dotenv
import logging
import time # Optional: for timing debug

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# --- Google API Key Setup (remains the same) ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    logger.error("GOOGLE_API_KEY not found in environment variables")
    # Use st.error for visibility in Streamlit if needed, but raising might be okay
    st.error("GOOGLE_API_KEY not found in environment variables!")
    raise EnvironmentError("GOOGLE_API_KEY environment variable is required")
# No need to set os.environ here if ChatGoogleGenerativeAI takes api_key directly
# os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Load clinic information
clinic_info = """
**About Lo Physiotherapy:**

Lo Physiotherapy began its journey in 1996 with a mission to provide professional and effective pain management solutions that are both affordable and accessible to the community. With 28 years of experience, over 400,000 patient visits, and 6 branches across Penang, their commitment remains strong. They address the growing challenge of back pain, which affects 8 out of 10 people globally, by offering precise diagnostic services, effective treatments, and patient education for sustainable lifestyle habits. Lo Physiotherapy believes everyone deserves a healthy and fulfilling life and strives to make a difference daily, one patient at a time.

**Our Physiotherapy Philosophy (H.E.A.R.T.S):**

At Lo Physiotherapy, the patient is at the heart of everything they do. Their philosophy is built on the acronym H.E.A.R.T.S, which stands for:

*   Healing: Focusing on the patient's overall well-being and recovery.
*   Evidence: Utilizing evidence-based practices, combining scientific research with clinical experience to tailor effective treatment plans.
*   Accurate Diagnosis: Laying the foundation for a healing journey by identifying the underlying cause of discomfort through comprehensive assessments.
*   Relationships: Building long-term connections and partnerships with patients, adapting to their evolving needs.
*   Teamwork: Collaborating for increased accountability, pooling expertise to ensure no aspect of health is overlooked.
*   Sustainability: Empowering patients with knowledge and habits for lasting health benefits, promoting long-term well-being.

**Conditions Treated:**

Lo Physiotherapy specializes in treating a wide range of conditions, including:

*   Neck Pain & Headache
*   Shoulder, Elbow & Arm Pain
*   Back Pain
*   Sciatica
*   Slipped Disc
*   Knee Pain
*   Plantar Fasciitis, Ankle & Foot Pain

**Treatment Approaches:**

Lo Physiotherapy provides evidence-based physiotherapy, offering various treatment methods tailored to individual needs:

*   Spinal Instrument Adjustment: Enhances spinal alignment, joint mobility, and nerve function.
*   Manual Therapy: Hands-on techniques to alleviate pain and restore function in the musculoskeletal system.
*   Medical Acupuncture: Science-based acupuncture targeting specific conditions, relieving pain, and promoting recovery.
*   Dry Needling: Targets tight muscle areas (trigger points) to ease muscle tension and pain.
*   Exercise Therapy: Customized physical activities to improve health and address specific conditions.
*   Shockwave Therapy: Uses sound waves to accelerate the body's healing in tendons, ligaments, and soft tissues.
*   Interferential Therapy: Employs medium-frequency electrical stimulation to treat pain, diminish inflammation, and encourage recovery.
*   Ultrasound Therapy: Promotes healing, eases pain, and enhances mobility in musculoskeletal issues.
*   Traction Therapy: Eases pressure on discs and nerves by gently stretching joints, especially in the spine.
*   Parkinson Rehabilitation: Customised program to address both motor and non-motor symptoms, minimizing symptoms and enhancing life quality

**Symptoms Addressed and Treatment Approaches:**

*   **Stiff & painful muscles:** Lo Physiotherapy uses manual therapy, dry needling, and exercise therapy to release muscle tension, reduce pain, and improve mobility.
*   **Pain from work or workouts:** Treatment plans are tailored to address the specific causes of pain, often involving manual therapy, exercise therapy, and modalities like ultrasound or interferential therapy to promote healing and reduce inflammation.
*   **Neck pain from sitting too much:** Spinal instrument adjustment, manual therapy, and exercise therapy are used to correct posture, improve spinal alignment, and alleviate neck pain.
*   **Backache from prolonged sitting, standing, and working:** Treatment focuses on spinal decompression, manual therapy, and core strengthening exercises to reduce pressure on the spine and improve back support.
*   **Numbness on your arm and leg:** Neural mobilization techniques, manual therapy, and spinal adjustments are used to address nerve compression and improve nerve function.
*   **Shoulder pain in your daily activity:** Shoulder joint instrument adjustment, manual therapy, and targeted exercises are used to improve shoulder mobility, reduce pain, and restore function.
*   **Knee pain at early morning, raise from prolong siting and up or down stair cases:** Knee joint instrument adjustment, manual therapy, and strengthening exercises are used to improve knee alignment, reduce pain, and enhance mobility.
*   **Heel pain at early morning wake up, raise from prolong sitting and walking:** Manual therapy, dry needling, custom-made orthotics/insoles, and specific exercises are used to address plantar fasciitis, reduce pain, and improve foot biomechanics.

**Locations and Contact Information:**

*   **Lo Physiotherapy Tanjong Tokong branch:** [Location] C-1-6 Vantage (Level 1), Jalan Desiran Tanjong, 10470 Tanjong Tokong, Penang. [Opening Hours] Mon - Thurs: 9.30am - 9pm, Fri: 9.30am - 6pm, Sat: 8.30am - 5pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 016-9341230, 012-5297825.
*   **Lo Physiotherapy Georgetown Specialist Hospital branch:** [Location] 2A, Jalan Masjid Negeri, 11900, Georgetown, Penang. [Opening Hours] Mon & Thurs: 9.30am - 8pm, Tue & Wed: 9.30am - 6pm, Fri: 9.30am - 5pm, Sat: 8.30am - 5pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 017-9123081.
*   **Lo Physiotherapy Kek Lok Si Charitable Hospital branch:** [Location] 623, Jalan Balik Pulau, Penang Ayer Itam, 11500 Ayer Itam, Penang. [Opening Hours] Mon & Thurs: 9.30am - 8pm, Tue & Wed: 9.30am - 6pm, Fri: 9.30am - 5pm, Sat: 8.30am - 1pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 016-5293996.
*   **Lo Physiotherapy Raja Uda branch:** [Location] Block A-79, Jalan Raja Uda, Pusat Perniagaan Raja Uda, 12300 Butterworth, Penang. [Opening Hours] Mon, Wed & Thurs: 9.30am - 8.30pm, Tue & Fri: 9.30am - 6pm, Sat: 9am - 5pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 016-8869934.
*   **Oh Physiotherapy Bayan Lepas branch:** [Location] 1-2-20 Kompleks I-Avenue, Bukit Jambul, Bayan Lepas, Penang. [Opening Hours] Mon & Wed: 9.30am - 8pm, Tue & Thurs: 9.30am - 7pm, Fri: 9.30am - 6pm, Sat: 8.30am - 4pm. Lunch hour: 1pm - 2pm (except Saturday). [Contacts] Tel: 04-6410850.
*   **Oh Physiotherapy B BRAUN Factory branch:** [Location] Bayan Lepas Industrial Park, 10810 Bayan Baru, Penang. [Opening Hours] BY APPOINTMENT ONLY. Tue & Wed: 2pm - 4pm, Thurs: 9.30am - 12pm. Tel: 016-4337780.

**Contact Information:**

*   Phone: +6012-529 7825
"""

# --- Cached Function for Vector Store ---
@st.cache_resource # Decorator to cache the returned object
def load_vector_store():
    """Loads or creates the vector store, cached for the session."""
    logger.info("Attempting to load/create vector store (will run only once per session)...")
    start_time = time.time()
    try:
        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(clinic_info)
        logger.info(f"Split text into {len(chunks)} chunks.")

        # Create embeddings (this model loading might also benefit from caching if slow,
        # but HuggingFaceEmbeddings might handle internal caching)
        logger.info("Loading embedding model...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        logger.info("Embedding model loaded.")

        # Create vector store
        logger.info("Creating FAISS index...")
        # If you previously saved index files, load them here instead for speed
        # Example: vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        # If creating from scratch:
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        logger.info("FAISS index created.")

        end_time = time.time()
        logger.info(f"Vector store loaded/created successfully in {end_time - start_time:.2f} seconds.")
        return vectorstore
    except Exception as e:
        logger.error(f"FATAL: Error creating vector database: {e}", exc_info=True)
        st.error(f"Failed to initialize knowledge base: {e}")
        # Depending on desired behavior, you might return None or raise the exception
        # Returning None might allow the app to run without RAG features
        # Raising will stop the app, forcing the issue to be fixed.
        raise # Let's raise to make sure it's addressed

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
vectorstore = load_vector_store()
llm = load_llm()

# --- Language Detection (remains the same) ---
def detect_language(text):
    # ... (your existing detect_language function) ...
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
# ... (your prompt definitions and prompts dictionary) ...
# Define prompts for each language
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

# Create a dictionary to store the prompts
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

# --- Memory Setup ---
# NOTE: This still resets on each run. For true conversational memory in Streamlit,
# you should manage history in st.session_state and pass it into get_response.
# We'll leave this for now to fix the blank screen, but it's the next thing to improve.
memories = {
    'english': ConversationBufferWindowMemory(k=10, return_messages=True),
    'chinese': ConversationBufferWindowMemory(k=10, return_messages=True),
    'malay': ConversationBufferWindowMemory(k=10, return_messages=True)
}
current_language = 'english' # This might also need session_state if you want language to persist

# # --- get_response Function (Add more logging and ensure it uses cached llm/vectorstore) ---
# def get_response(query):
#     global current_language # Consider managing this via session_state too
#     global vectorstore # Access cached vectorstore
#     global llm # Access cached llm
#     global memories # Access module-level memory (see note above)

#     logger.info(f"--- Starting get_response for query: '{query}' ---")

#     if not query or query.strip() == "":
#         logger.warning("Empty query received in get_response")
#         return "Please ask a question so I can assist you."

#     # Ensure resources are loaded (should be cached, but check)
#     if not vectorstore or not llm:
#         logger.error("FATAL: Vectorstore or LLM not available in get_response!")
#         st.error("Core components (AI model or knowledge base) are not loaded. Cannot respond.")
#         return "I'm sorry, I cannot process your request right now due to an internal setup issue."

#     try:
#         # 1. Detect language
#         logger.info("Detecting language...")
#         detected_language = detect_language(query)
#         current_language = detected_language # Update global state (or better: session state)
#         logger.info(f"Language detected: {current_language}")

#         today = datetime.now().strftime("%A, %d %B %Y")

#         # 2. Retrieve context
#         logger.info("Searching vector store...")
#         start_search_time = time.time()
#         docs = vectorstore.similarity_search(query, k=4)
#         context = "\n\n".join([doc.page_content for doc in docs])
#         end_search_time = time.time()
#         logger.info(f"Vector store search completed in {end_search_time - start_search_time:.2f} seconds.")

#         # 3. Format chat history (using the volatile module-level memory)
#         logger.info("Formatting chat history from module memory...")
#         chat_history = ""
#         # Use try-except block for safety in case memory object is problematic
#         try:
#              messages = memories[current_language].chat_memory.messages
#              for message in messages:
#                   if message.type == "human":
#                       chat_history += f"User: {message.content}\n"
#                   else:
#                       chat_history += f"Assistant: {message.content}\n"
#              logger.info("Chat history formatted.")
#         except Exception as mem_e:
#              logger.error(f"Error formatting chat history: {mem_e}", exc_info=True)
#              chat_history = "Error retrieving chat history." # Provide fallback

#         # 4. Prepare and run LLM Chain
#         prompt = prompts[current_language]
#         logger.info("Creating LLM chain...")
#         llm_chain = LLMChain(llm=llm, prompt=prompt) # Use cached llm
#         logger.info("Running LLM chain...")
#         start_llm_time = time.time()
#         response = llm_chain.run(
#             chat_history=chat_history,
#             date=today,
#             context=context,
#             question=query
#         )
#         end_llm_time = time.time()
#         logger.info(f"LLM chain execution finished in {end_llm_time - start_llm_time:.2f} seconds.")

#         # 5. Update memory (module-level again)
#         try:
#             logger.info("Updating module memory...")
#             memories[current_language].chat_memory.add_user_message(query)
#             memories[current_language].chat_memory.add_ai_message(response)
#             logger.info("Module memory updated.")
#         except Exception as mem_e:
#             logger.error(f"Error updating memory: {mem_e}", exc_info=True)


#         logger.info(f"--- Successfully generated response in {current_language} ---")
#         return response

#     except Exception as e:
#         # Log the full error traceback
#         logger.error(f"!!! UNEXPECTED ERROR IN get_response !!!: {e}", exc_info=True)
#         st.error("An unexpected error occurred while processing your request.") # Show error in UI
#         return f"I'm truly sorry, but I encountered an unexpected technical difficulty. Please try asking again in a moment."

# # --- Functions to clear memory and get language (remain the same for now) ---
# def clear_memories():
#     """Clear conversation memory for all languages"""
#     global memories # Access module-level memory
#     try:
#         for lang in memories:
#             memories[lang].clear()
#         logger.info("All module-level conversation memories cleared")
#     except Exception as e:
#         logger.error(f"Error clearing memories: {e}", exc_info=True)


# def get_current_language():
#     """Return the current language being used"""
#     global current_language
#     return current_language

# --- DUMMY get_response ---
def get_response(query):
    logger.info(f"--- DEBUG: DUMMY get_response received query: '{query}' ---")
    # !! DO NOT call vectorstore, llm, detect_language, memory !!
    time.sleep(0.5) # Simulate tiny delay
    response = f"DEBUG: Dummy response for query: '{query}'"
    logger.info(f"--- DEBUG: DUMMY get_response returning: '{response}' ---")
    return response

# --- DUMMY clear_memories (if called by frontend) ---
def clear_memories():
    logger.info("--- DEBUG: DUMMY clear_memories called ---")
    pass

# --- DUMMY get_current_language (if called by frontend) ---
def get_current_language():
    logger.info("--- DEBUG: DUMMY get_current_language called ---")
    return "english" # Or any fixed value

# --- Local Test Block (remains the same) ---
if __name__ == "__main__":
    print("Lo Physiotherapy Multilingual Assistant (Type 'exit' to quit)")
    print("Supports: English, Chinese (中文), and Malay (Bahasa Melayu)")
    print("="*70)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            break

        response = get_response(user_input)
        print(f"\nAssistant: {response}")