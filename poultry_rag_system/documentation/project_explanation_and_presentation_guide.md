# 🐔 Poultry Care AI — Project Guide & Presentation Manual

This document provides a detailed overview of the project idea, a deep-dive walkthrough of a critical project file (`app/rag/pipeline.py`), and a comprehensive guide on how to pitch and defend this project in presentations (vivas).

---

## 1. Project Idea & Concept Outline

### 🔴 The Problem
1. **Economic Vulnerability:** In Egypt and many developing nations, poultry farming is a cornerstone of rural economies. Disease outbreaks (such as Newcastle Disease, Coccidiosis, and Salmonella) can wipe out entire flocks in days, causing devastating financial losses.
2. **Veterinary Scarcity:** Smallholder farmers often lack access to timely, affordable veterinary consults.
3. **Information Barrier:** Scientific manuals and disease guidelines are complex, bilingual, or locked in PDFs that are difficult for average farmers to search, read, or translate into actionable steps.

### 🟢 The Solution (PoultryCare AI)
PoultryCare AI is a hybrid intelligent decision-support system that combines:
1. **Computer Vision (TensorFlow/Keras):** Instantly diagnoses diseases from photos of birds or their droppings.
2. **Retrieval-Augmented Generation (RAG):** Dynamically searches a local vetted database of veterinary PDFs/DOCXs using semantic embeddings, then synthesizes a tailored treatment and prevention plan.
3. **Egyptian Arabic Localization:** The system speaks the local Egyptian dialect ("العامية المصرية"), formatting output with intuitive emojis and structure, bridging the gap between high-level science and rural farmers.

---

## 2. In-Depth Explanation of a Key File: `app/rag/pipeline.py`

The `app/rag/pipeline.py` file is the **central orchestrator** of the text-based Q&A (RAG) system. It ties together the database retriever, the cross-encoder reranker, prompt construction, memory management, and API calls.

### 🔍 Detailed Code Walkthrough

#### 1. Conversation Memory (`ConversationMemory` Class)
```python
class ConversationMemory:
    def __init__(self):
        self._history: dict[str, list[dict]] = {}
        self._max_turns = 10
```
* **Why it exists:** LLMs are stateless. To support follow-up questions (e.g., Q1: "What is Newcastle disease?" Q2: "How to treat it?"), the system needs memory.
* **Mechanism:** It stores conversation turns in-memory, mapped by a `session_id`. It limits the history to the last 10 turns (`_max_turns`) to prevent bloating the LLM's context window and incurring high API token costs.

#### 2. RAG Orchestration (`RAGPipeline` Class)
```python
class RAGPipeline:
    def __init__(self, retriever: Retriever | None = None, reranker: Reranker | None = None):
        self.retriever = retriever or Retriever()
        self.reranker = reranker or Reranker()
        ...
```
On initialization, it instantiates the Retriever (which communicates with the local JSON vector store) and the Reranker (which loads the Cross-Encoder model). It also initializes the OpenAI client pointing to the **OpenRouter API** endpoint.

#### 3. Execution Flow: `answer_question()`
This function executes the complete RAG loop when a user types a question:
1. **Retrieve History:** Fetches the last few messages for the current session.
2. **Retrieve Context (Bi-Encoder Search):** Embeds the user question using `paraphrase-multilingual-MiniLM-L12-v2` and searches the database for the top 5 most similar chunks.
3. **Rerank Context (Cross-Encoder Search):** Passes the 5 chunks to `cross-encoder/ms-marco-MiniLM-L-6-v2` alongside the query. The cross-encoder re-scores them and selects the top 3 most relevant.
4. **Build Prompt:** Sends the query, history, and top 3 chunks to `build_qa_prompt` to generate system and user messages.
5. **Call LLM with Exponential Backoff:** Sends the prompt to `openai/gpt-4o-mini` via OpenRouter.
6. **Post-Processing (Section Extraction):** Parses the generated text to extract only the requested section (e.g., if the user asked only about "treatment", it strips away "causes" and "symptoms").
7. **Update Memory:** Saves the turn to the in-memory history.

#### 4. Transient Error Handling & Resilient Fallback
```python
TRANSIENT_ERROR_PATTERNS = (
    "compaction worker", "empty response", "rate limit", "timeout",
    "service unavailable", "internal server error", "bad gateway", "gateway timeout",
)
```
* **Robustness:** If the OpenRouter API is rate-limited or times out, the `_call_llm` method catches the error, checks if it's a transient failure, and retries up to 3 times using exponential backoff (`1.0 * (2 ** attempt)` seconds delay).
* **Fallback Mode:** If the API fails completely after all retries, the pipeline doesn't crash. It falls back to `_format_fallback_response()`, which extracts the top raw text matches from the knowledge base and displays them directly to the user with a message indicating that the AI generation is temporarily unavailable.

#### 5. Dynamic Section Extraction (`_extract_relevant_section`)
If a user asks: *"ما هو علاج الكوكسيديا؟"* (What is the treatment for Coccidiosis?), they do not want to scroll through pages explaining causes or symptoms. This function parses the Arabic response using regex keywords:
* It looks for headers like `💊 العلاج:` and extracts only that paragraph until it hits the next header (e.g., `🛡️ الوقاية:`). This ensures concise, high-value answers.

---

## 3. How to Present the Project in Presentations (Slides/Viva Guide)

### 📊 Suggested Presentation Slide Structure

#### Slide 1: Title & Team
* **Title:** PoultryCare AI: An Intelligent Multi-Modal Assistant for Poultry Disease Diagnosis & Retrieval.
* **Subtitle:** Combining TensorFlow Image Classification & Cross-Encoder Reranked RAG.
* **Visual:** Screenshot of the Streamlit dashboard or a poultry diagnostic flowchart.

#### Slide 2: The Problem
* **Key Bullet Points:**
  * Poultry diseases cause catastrophic financial losses in Egyptian farms.
  * Shortage of veterinary specialists in rural areas.
  * Scientific information is scattered and hard for farmers to read or query.
* **Why Traditional AI Fails:** Large Language Models (like GPT) have knowledge cutoffs, hallucinate clinical treatments, and lack domain-specific Arabic vet data.

#### Slide 3: The Solution (Architecture Concept)
* Explain the two-pillar approach:
  * **Pillar 1 (Vision):** TensorFlow model runs instant diagnostic classification on droppings/birds.
  * **Pillar 2 (RAG):** Custom local search retrieves vetted scientific literature, and the LLM translates it into dialect.

#### Slide 4: System Architecture (The Technical Flowchart)
* Show a diagram of the data flow:
  * Streamlit (UI) $\rightarrow$ FastAPI (endpoints) $\rightarrow$ RAG Pipeline / Vision Predictor.
  * **Ingestion:** PDF/DOCX $\rightarrow$ PyMuPDF/Tesseract OCR $\rightarrow$ Normalization $\rightarrow$ Sentence Chunks $\rightarrow$ Sentence-Transformers $\rightarrow$ JSON Vector Store.

#### Slide 5: The Computer Vision Classifier
* **Input size:** $224 \times 224 \times 3$ (RGB).
* **Classes:** Coccidiosis, Salmonella, Newcastle Disease, Healthy.
* **Core Highlight:** **Confidence Threshold (40%).** Explain that if confidence is below 40%, the system triggers a veterinary consult warning rather than guessing, ensuring biosecurity safety.

#### Slide 6: The RAG Pipeline Deep Dive
* Explain the **two-stage retrieval** process:
  1. **Stage 1 (Embedding Search):** Multilingual MiniLM embeddings search the vector space (fast).
  2. **Stage 2 (Reranking):** Cross-Encoder ms-marco model evaluates context relevance (highly accurate).
* **Benefit:** Reduces LLM hallucinations and maximizes information density.

#### Slide 7: Memory & Persistence
* Explain **Session Memory** (capturing context for conversation flow) and **SQLite Database logging** (persisting chat history and diagnoses forever for farm audits).

#### Slide 8: The Live Demo
* Open the Streamlit application:
  1. Show the **Dashboard** with statistics.
  2. Upload an image of Coccidiosis to showcase the automatic image classification leading to RAG-grounded treatments.
  3. Go to the **AI Assistant** and ask a follow-up question in Egyptian Arabic.

#### Slide 9: Future Scope & Scaling
* Switch from JSON Vector Store to ChromaDB/FAISS.
* Deploy using Docker containers.
* Support additional disease classes (e.g., Avian Influenza, Gumboro).

---

## 4. Key Defense Strategies for the Viva (Questions & Answers)

Here are the most common traps professors set and how to handle them:

### 💬 Q1: Why did you use a local JSON file as a vector store instead of ChromaDB or Pinecone?
* **Answer:** *"For the prototype phase, our knowledge base consists of under 1000 chunks. Using a JSON-backed store with NumPy cosine similarity eliminated server setup dependencies, allowed easy inspection during debugging, and was extremely lightweight. However, the system is designed with a clean interface (`VectorStore` class), so switching to ChromaDB in production requires replacing just one module without changing the API."*

### 💬 Q2: Why not just fine-tune an LLM on the poultry PDFs instead of using RAG?
* **Answer:** *"Fine-tuning is expensive, time-consuming, and does not solve hallucinations. If a new disease treatment or vaccine protocol comes out, we would have to retrain the model. With RAG, we can simply drop the new PDF into the folder, and it gets indexed immediately. Additionally, RAG allows us to show source citations (which PDF and page number), which is critical for veterinary accountability."*

### 💬 Q3: What is the purpose of the Rerank stage? Why not just use the embedding search?
* **Answer:** *"Embedding models (Bi-encoders) look at queries and documents independently. While fast, they can overlook key context. A Cross-encoder evaluates the query and document together, paying attention to specific interactions. By using the Bi-encoder to fetch the top 5 chunks and the Cross-encoder to rerank them down to 3, we combine the speed of the first with the accuracy of the second."*

### 💬 Q4: How does the system handle scanned/image-based PDFs?
* **Answer:** *"Standard libraries like `pypdf` fail when a PDF is scanned. Our loader checks the character count of the output. If it is less than 500 characters, it triggers our OCR fallback: it renders pages as images using PyMuPDF (fitz) at 300 DPI, then calls Tesseract OCR configured with the `ara+eng` language packet to extract both Arabic and English text."*
