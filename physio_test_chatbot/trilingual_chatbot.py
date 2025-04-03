import os
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from datetime import datetime, date
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

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

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
chunks = text_splitter.split_text(clinic_info)

# Create embeddings and vector store
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

# Define language detection function
def detect_language(text):
    """Detect the language of the input text."""
    try:
        lang = detect(text)
        # Map language codes to our supported languages
        if lang == 'zh-cn' or lang == 'zh-tw' or lang == 'zh':
            return 'chinese'
        elif lang == 'ms' or lang == 'id':  # Indonesian is similar to Malay
            return 'malay'
        else:
            return 'english'  # Default to English for other languages
    except LangDetectException:
        return 'english'  # Default to English if detection fails

# Define prompts for each language
english_prompt_template = """
You are a helpful assistant for Lo Physiotherapy clinic in Penang, Malaysia. You provide information about the clinic's services, treatments, locations, and answer common patient questions.

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

# Set up the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3, api_key=os.getenv("GOOGLE_API_KEY"))

# Set up memory - we'll use separate memories for each language
memories = {
    'english': ConversationBufferMemory(return_messages=True),
    'chinese': ConversationBufferMemory(return_messages=True),
    'malay': ConversationBufferMemory(return_messages=True)
}

# Current language tracker
current_language = 'english'  # Default language

def get_response(query):
    """Get a response from the chatbot in the appropriate language."""
    global current_language
    
    # Detect language of the query
    detected_language = detect_language(query)
    current_language = detected_language
    
    today = datetime.now().strftime("%A, %d %B %Y")
    
    # Get relevant documents
    docs = vectorstore.similarity_search(query)
    
    # Format the context from documents
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Format chat history
    chat_history = ""
    messages = memories[current_language].chat_memory.messages
    for message in messages:
        if message.type == "human":
            chat_history += f"User: {message.content}\n"
        else:
            chat_history += f"Assistant: {message.content}\n"
    
    # Get the appropriate prompt for the detected language
    prompt = prompts[current_language]
    
    # Create the LLM chain
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Get the response
    response = llm_chain.run(
        chat_history=chat_history,
        date=today,
        context=context,
        question=query
    )
    
    # Update memory for the current language
    memories[current_language].chat_memory.add_user_message(query)
    memories[current_language].chat_memory.add_ai_message(response)
    
    return response

# Test the chatbot
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