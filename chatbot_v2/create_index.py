# --- START OF FILE create_index.py ---
import os
import logging
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import time

# --- Configuration ---
INDEX_SAVE_PATH = "faiss_index"  # Folder where the index will be saved
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 200

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Load Environment Variables (Optional, if needed for anything else) ---
load_dotenv()

# --- Clinic Information Text (Copy from your original file) ---
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
*   **Heel pain at early morning wake up, raise from prolong sitting and walking:** Manual therapy, dry newedling, custom-made orthotics/insoles, and specific exercises are used to address plantar fasciitis, reduce pain, and improve foot biomechanics.

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

# --- Function to Create and Save Index ---
def create_and_save_vectordb(save_path=INDEX_SAVE_PATH):
    """Creates and saves a FAISS vector database from the clinic information."""
    logger.info(f"Starting index creation process. Saving to '{save_path}'...")
    start_time = time.time()
    try:
        # 1. Split the text into chunks
        logger.info("Splitting text...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
        chunks = text_splitter.split_text(clinic_info)
        logger.info(f"Split text into {len(chunks)} chunks.")
        if not chunks:
            raise ValueError("Text splitting resulted in zero chunks. Check clinic_info content.")

        # 2. Create embeddings
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        logger.info("Embedding model loaded.")

        # 3. Create FAISS index from texts
        logger.info("Creating FAISS index from text chunks...")
        vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)
        logger.info("FAISS index created in memory.")

        # 4. Save the index to disk
        logger.info(f"Saving FAISS index to directory: {save_path}...")
        os.makedirs(save_path, exist_ok=True) # Ensure directory exists
        vectorstore.save_local(save_path)
        logger.info(f"FAISS index saved successfully to {save_path}.")

        end_time = time.time()
        logger.info(f"Index creation and saving completed in {end_time - start_time:.2f} seconds.")

    except Exception as e:
        logger.error(f"Error during index creation/saving: {e}", exc_info=True)
        raise # Re-raise the exception after logging

# --- Main Execution Block ---
if __name__ == "__main__":
    logger.info("Running FAISS index creation script...")
    create_and_save_vectordb()
    logger.info("Script finished.")
# --- END OF FILE create_index.py ---