# 🐔 Poultry Disease RAG System — Viva Defense Guide
# دليل مناقشة مشروع نظام RAG لأمراض الدواجن

---

## 📋 Table of Contents / فهرس المحتويات

1. [Project Overview / نظرة عامة على المشروع](#1-project-overview--نظرة-عامة-على-المشروع)
2. [System Architecture / بنية النظام](#2-system-architecture--بنية-النظام)
3. [Module-by-Module Explanation / شرح كل وحدة بالتفصيل](#3-module-by-module-explanation--شرح-كل-وحدة-بالتفصيل)
4. [RAG Pipeline Deep Dive / تحليل معمارية RAG](#4-rag-pipeline-deep-dive--تحليل-معمارية-rag)
5. [Vision Pipeline Deep Dive / تحليل معمارية الرؤية](#5-vision-pipeline-deep-dive--تحليل-معمارية-الرؤية)
6. [Database Design / تصميم قاعدة البيانات](#6-database-design--تصميم-قاعدة-البيانات)
7. [API Design / تصميم واجهة البرمجة](#7-api-design--تصميم-واجهة-البرمجة)
8. [Frontend (Streamlit) / الواجهة الأمامية](#8-frontend-streamlit--الواجهة-الأمامية)
9. [Important Comparisons / مقارنات مهمة](#9-important-comparisons--مقارنات-مهمة)
10. [Identified Bugs & Fixes / الأخطاء المكتشفة والحلول](#10-identified-bugs--fixes--الأخطاء-المكتشفة-والحلول)
11. [25 Professor Questions & Answers / 25 سؤال من المُحاضر مع الإجابات](#11-25-professor-questions--answers--25-سؤال-من-المحاضر-مع-الإجابات)
12. [Viva Cheat Sheet / ورقة غش المناقشة](#12-viva-cheat-sheet--ورقة-غش-المناقشة)

---

## 1. Project Overview / نظرة عامة على المشروع

### English

The **Poultry Disease RAG System** is an AI-powered assistant designed for Egyptian poultry farmers, veterinarians, and agricultural specialists. It combines two core AI capabilities:

1. **Retrieval-Augmented Generation (RAG)** — Answers natural-language questions about poultry diseases using a knowledge base of veterinary PDFs/DOCXs, retrieved semantically via vector embeddings and answered by an LLM (OpenRouter/GPT-4o-mini).

2. **Image-Based Disease Diagnosis** — A TensorFlow/Keras deep learning classifier predicts the most likely disease from an uploaded poultry image (Coccidiosis, Healthy, New Castle Disease, Salmonella), and the RAG pipeline then explains symptoms, causes, treatment, and prevention in Egyptian Arabic.

### Arabic (العربية)

مشروع **نظام RAG لأمراض الدواجن** هو مساعد ذكي مصمم لمربى الدواجن في مصر والأطباء البيطريين وأخصائيي الزراعة. يجمع بين قدرتين أساسيتين:

1. **الاسترجاع المعزز بالتوليد (RAG)** — يجيب على الأسئلة بلغة طبيعية حول أمراض الدواجن باستخدام قاعدة معرفة من ملفات PDF/DOCX بيطري، يتم استرجاعها دلالياً عبر تضمينات المتجهات ويتم الإجابة عليها بواسطة نموذج لغوي كبير (OpenRouter/GPT-4o-mini).

2. **تشخيص الأمراض من الصور** — يتنبأ مصنف التعلم العميق (TensorFlow/Keras) بالمرض الأكثر احتمالاً من صورة دواجن مرفوعة (الكوكسيديا، صحي، مرض نيوكاسل، السلمونيلا)، ثم يشرح خط أنابيب RAG الأعراض والأسباب والعلاج والوقاية باللهجة المصرية.

### Key Features / المميزات الرئيسية

| Feature / الميزة | Description / الوصف |
|---|---|
| Bilingual Support | Arabic-first with English codebase |
| RAG Pipeline | Semantic search + LLM generation |
| Image Classification | 4-class TensorFlow model |
| Conversation Memory | Per-session history (10 turns) |
| Graceful Degradation | Falls back to raw context if LLM fails |
| OCR Fallback | PyMuPDF + Tesseract for scanned PDFs |
| Cross-Encoder Reranking | Improves retrieval precision |

### Tech Stack / التقنيات المستخدمة

```
Backend:        FastAPI + Uvicorn
Frontend:       Streamlit
Vector Store:   Custom JSON-backed (with cosine similarity)
Embeddings:     sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)
Reranker:       cross-encoder/ms-marco-MiniLM-L-6-v2
LLM:            OpenRouter (openai/gpt-4o-mini)
Vision:         TensorFlow/Keras image classifier
Database:       SQLite (chat & diagnosis history)
OCR:            PyMuPDF + Tesseract
```

---

## 2. System Architecture / بنية النظام

### High-Level Architecture / البنية العامة

```
┌─────────────────────────────────────────────────────────┐
│                    STREAMLIT FRONTEND                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │Dashboard │ │Assistant │ │  Image   │ │ Disease   │  │
│  │          │ │  (Chat)  │ │ Analysis │ │ Library   │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └───────────┘  │
│       │            │            │                        │
└───────┼────────────┼────────────┼────────────────────────┘
        │            │            │
        ▼            ▼            ▼
┌─────────────────────────────────────────────────────────┐
│                   FASTAPI BACKEND                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                │
│  │/chat/    │ │/image/   │ │/upload/  │                │
│  │          │ │diagnose  │ │pdf       │                │
│  └────┬─────┘ └────┬─────┘ └──────────┘                │
│       │            │                                     │
│       ▼            ▼                                     │
│  ┌─────────────────────────────┐                        │
│  │      RAGPipeline            │                        │
│  │  Retriever → Reranker →     │                        │
│  │  PromptBuilder → LLM        │                        │
│  └──────────┬──────────────────┘                        │
│             │                                            │
│  ┌──────────▼──────┐  ┌──────────────┐                  │
│  │  VectorStore    │  │  Predictor   │                  │
│  │  (JSON + cosine)│  │  (TF Model)  │                  │
│  └─────────────────┘  └──────────────┘                  │
│                                                          │
│  ┌─────────────────┐                                    │
│  │  SQLite History  │                                    │
│  └─────────────────┘                                    │
└─────────────────────────────────────────────────────────┘
```

### RAG Pipeline Flow / تدفق خط أنابيب RAG

```
User Question (Arabic)
        │
        ▼
┌─────────────────┐
│   Retriever     │  ← Semantic search via embeddings
│   (top_k=5)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Reranker      │  ← Cross-encoder re-scoring
│   (top_k=3)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Prompt Builder  │  ← System prompt + context + history
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LLM Call      │  ← OpenRouter (GPT-4o-mini)
│   (with retry)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Section Extract │  ← Extract relevant section
└────────┬────────┘
         │
         ▼
    Arabic Answer
```

### Vision Pipeline Flow / تدفق خط أنابيب الرؤية

```
Image Upload (JPG/PNG)
        │
        ▼
┌─────────────────┐
│  Preprocessing  │  ← Resize (224×224) + Normalize
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TF Classifier  │  ← 4 classes: Coccidiosis, Healthy,
│  (Keras model)  │     New Castle Disease, Salmonella
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Confidence     │  ← If < 40%, warn user
│  Check          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG Pipeline   │  ← explain_diagnosis(disease, conf)
│  (retrieve +    │
│   rerank + LLM) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Arabic Format  │  ← Structured: diagnosis, causes,
│  (Explainer)    │     symptoms, treatment, prevention
└────────┬────────┘
         │
         ▼
    Arabic Diagnosis
```

---

## 3. Module-by-Module Explanation / شرح كل وحدة بالتفصيل

### 3.1 Core Module / وحدة النواة

#### `app/core/config.py` — Configuration / الإعدادات

**What it does / ماذا يفعل:**
Centralizes all configuration. Loads secrets from Streamlit Secrets first, falls back to environment variables. Never hardcodes API keys.

يمركز كل الإعدادات. يحمل الأسرار من Streamlit Secrets أولاً، ثم ينتقل إلى متغيرات البيئة كبديل. لا يضع مفاتيح API في الكود أبداً.

```python
@dataclass(frozen=True)
class Settings:
    openrouter_api_key: str | None
    openrouter_model: str          # default: "openai/gpt-4o-mini"
    google_api_key: str | None
    hf_token: str | None
    chroma_db_path: str            # default: "./vector_db"
    model_path: str                # default: "./models/poultry_classifier.keras"
    tessdata_prefix: str
    chunk_size: int = 450          # RAG tuning
    chunk_overlap: int = 200       # RAG tuning
    retriever_top_k: int = 5       # RAG tuning
    reranker_top_k: int = 3        # RAG tuning
    image_size: tuple = (224, 224) # Vision tuning
    disease_classes: tuple = (     # Must match model output
        "Coccidiosis", "Healthy",
        "New Castle Disease", "Salmonella"
    )
```

**Key Design Decision / قرار تصميم مهم:**
Uses `@lru_cache` to load settings once per process. Uses `_get_secret()` helper that tries `st.secrets` first, then `os.environ`.

#### `app/core/logger.py` — Logging / التسجيل

**What it does / ماذا يفعل:**
Provides a shared logger with consistent formatting across all modules.

```python
def get_logger(name: str) -> logging.Logger:
    # Format: "2026-08-27 10:30:00 | INFO     | app.rag.pipeline | Message"
```

#### `app/core/utils.py` — Utilities / الأدوات المساعدة

**What it does / ماذا يفعل:**
Contains shared utility functions:
- `file_hash()` — SHA-256 hash for PDF deduplication
- `ensure_dir()` — Create directories if they don't exist
- `Timer` — Context manager for timing code blocks
- `Translator` — English-to-Arabic translator using `deep-translator`

---

### 3.2 RAG Module / وحدة RAG

#### `app/rag/loader.py` — Document Loading / تحميل المستندات

**What it does / ماذا يفعل:**
Loads PDF and DOCX files from disk. For PDFs, tries `pypdf` first for clean text extraction. If text is too short (< 500 chars), falls back to OCR using PyMuPDF + Tesseract.

```python
def load_pdf(path) -> RawDocument:
    # 1. Try pypdf (fast, clean text)
    text, page_count = _extract_text_with_pypdf(pdf_path)
    # 2. If too short, try OCR fallback
    if len(text.strip()) < 500:
        ocr_text = _extract_text_with_ocr(pdf_path)
    # 3. Return RawDocument with metadata
```

**Key Feature / ميزة مهمة:**
- Supports both Arabic and English OCR (`lang="ara+eng"`)
- Cleans extracted text by removing duplicate sentences and noise artifacts
- Returns `RawDocument` dataclass with `source_path`, `text`, and `metadata`

#### `app/rag/preprocessing.py` — Text Cleaning / تنظيف النص

**What it does / ماذا يفعل:**
Cleans and normalizes raw document text before chunking. Handles:
- Unicode normalization (NFKC)
- Arabic noise patterns from corrupted PDF extraction
- Duplicate word/sentence removal
- Symbol cleaning
- Hyphenated word rejoining

```python
def clean_text(text: str) -> str:
    # 1. Unicode normalization
    # 2. Remove noise patterns (Arabic PDF artifacts)
    # 3. Remove noise words
    # 4. Deduplicate words
    # 5. Remove duplicate sentences
    # 6. Clean symbols
```

**Important Patterns / أنماط مهمة:**
```python
_NOISE_PATTERNS = [
    r"تم\s*إعداده\s*خصيصاً\s*للمربي\s*المصري",  # Vaccination guide noise
    r"الدليل\s*العلمي\s*الشامل\s*لأمراض",          # Management guide noise
    r"صفحة\s*\d+\s*من\s*\d+",                      # Page numbers
]
```

#### `app/rag/chunking.py` — Text Chunking / تقسيم النص

**What it does / ماذا يفعل:**
Splits cleaned text into overlapping chunks suitable for embedding. Uses sentence-aware splitting first, falls back to word-based splitting.

```python
@dataclass
class Chunk:
    text: str
    metadata: dict  # {"source": "file.pdf", "page": 3, "chunk_index": 2}

def chunk_text(text, metadata, chunk_size=450, chunk_overlap=200) -> list[Chunk]:
    # 1. Try sentence-based splitting (preferred)
    # 2. Fall back to word-based splitting with overlap
```

**Key Parameters / المعاملات الرئيسية:**
- `chunk_size=450` — Target chunk size (in characters, divided by 8 for word count)
- `chunk_overlap=200` — Overlap between consecutive chunks

#### `app/rag/embeddings.py` — Embedding Model / نموذج التضمين

**What it does / ماذا يفعل:**
Wraps `sentence-transformers` for semantic embeddings. Uses `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensions, supports Arabic + English).

```python
class EmbeddingModel:
    def __init__(self, model_name="paraphrase-multilingual-MiniLM-L12-v2"):
        self.dimension = 384

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        # Batch embedding for indexing

    def embed_query(self, query: str) -> list[float]:
        # Single query embedding for search
```

**Why this model? / لماذا هذا النموذج؟**
- Supports 50+ languages including Arabic
- Small size (≈120MB) — fast inference
- 384 dimensions — good balance of quality and speed

#### `app/rag/vector_store.py` — Vector Store / متجر المتجهات

**What it does / ماذا يفعل:**
A lightweight, local vector store backed by JSON on disk. Stores chunks with their embeddings and performs cosine similarity search.

```python
class VectorStore:
    def __init__(self, persist_directory, embedding_model):
        self._documents: list[dict] = []  # Loaded from JSON
        self._store_path = "poultry_disease_knowledge_base.json"

    def add_chunks(self, chunks: list[Chunk]):
        # Embed and upsert chunks

    def similarity_search(self, query: str, top_k=5) -> list[dict]:
        # Embed query, compute cosine similarity, return top_k
```

**Why JSON instead of ChromaDB? / لماذا JSON بدلاً من ChromaDB؟**
- Simpler deployment (no separate server)
- Easier to debug and inspect
- Sufficient for small-to-medium knowledge bases
- No additional dependencies

#### `app/rag/retriever.py` — Retriever / المسترجع

**What it does / ماذا يفعل:**
Takes a user query and returns the most relevant knowledge-base chunks. Has two entry points:
- `retrieve(query)` — General semantic search
- `retrieve_for_disease(disease_name)` — Specialized search for image diagnosis

```python
class Retriever:
    def retrieve(self, query, top_k=5) -> list[dict]:
        return self.vector_store.similarity_search(query, top_k)

    def retrieve_for_disease(self, disease_name, top_k=5) -> list[dict]:
        query = f"symptoms causes treatment prevention of {disease_name} in poultry"
        return self.retrieve(query, top_k)
```

#### `app/rag/reranker.py` — Reranker / إعادة الترتيب

**What it does / ماذا يفعل:**
Re-scores retrieved candidates using a cross-encoder model for better semantic relevance. Falls back to original order if the model fails.

```python
class Reranker:
    def rerank(self, query, candidates, top_k=3) -> list[dict]:
        # 1. Load cross-encoder model (lazy)
        # 2. Score (query, document) pairs
        # 3. Sort by score, return top_k
```

**Why Cross-Encoder? / لماذا مرمّز متقاطع؟**
- Bi-encoders (like sentence-transformers) encode query and document independently
- Cross-encoders see both together → more accurate relevance scoring
- Trade-off: slower, so we use it only on top-k candidates (not all documents)

#### `app/rag/prompt_builder.py` — Prompt Builder / بناء الموجه

**What it does / ماذا يفعل:**
Builds the final prompt sent to the LLM. Contains two system prompts:
- `SYSTEM_PROMPT_QA` — For general Q&A (Egyptian Arabic dialect)
- `SYSTEM_PROMPT_DIAGNOSIS` — For image diagnosis explanations

```python
def build_qa_prompt(question, context_chunks, history) -> list[dict]:
    # System prompt + conversation history + context + question

def build_diagnosis_prompt(disease_name, confidence, context_chunks) -> list[dict]:
    # System prompt + disease info + context
```

**Key Design / تصميم مهم:**
- All prompts are in Egyptian Arabic dialect (عامية مصرية)
- Structured output format with emoji headers (🐔, 🦠, 🔍, 💊, 🛡️, 📌)
- Includes disclaimer: "النتيجة دي معمولة بالذكاء الاصطناعي بهدف المساعدة، لكنها ما تغنيش عن تشخيص الطبيب البيطري"

#### `app/rag/pipeline.py` — RAG Pipeline / خط أنابيب RAG

**What it does / ماذا يفعل:**
Top-level orchestration: retrieve → rerank → build prompt → call LLM. Includes:
- Conversation memory (per-session, 10 turns max)
- Query caching (same query reuses results)
- Retry with exponential backoff (3 retries)
- Graceful fallback to raw context if LLM fails

```python
class RAGPipeline:
    def answer_question(self, question, session_id) -> dict:
        # 1. Get conversation history
        # 2. Retrieve + rerank (cached)
        # 3. Build QA prompt
        # 4. Call LLM (with retry)
        # 5. Extract relevant section
        # 6. Save to conversation memory
        return {"answer": response, "sources": top_chunks}

    def explain_diagnosis(self, disease_name, confidence) -> dict:
        # 1. Retrieve for disease
        # 2. Rerank
        # 3. Build diagnosis prompt
        # 4. Call LLM
        return {"disease": ..., "confidence": ..., "explanation": ..., "sources": ...}
```

**Transient Error Handling / معالجة الأخطاء المؤقتة:**
```python
TRANSIENT_ERROR_PATTERNS = (
    "compaction worker", "empty response", "rate limit",
    "timeout", "service unavailable", "internal server error",
    "bad gateway", "gateway timeout",
)
# Retry up to 3 times with exponential backoff (1s, 2s, 4s)
```

#### `app/rag/normalizer.py` — Text Normalization / تطبيع النص

**What it does / ماذا يفعل:**
Normalizes Arabic text and query terms by mapping variant spellings to canonical forms.

```python
_VARIANT_MAP = {
    "نيوكاسيل": "نيوكاسل",    # Variant → canonical
    "النيوكاسيل": "النيوكاسل",
    "اتش بي": "ايب",          # H.P. → IB
}
```

---

### 3.3 Vision Module / وحدة الرؤية

#### `app/vision/preprocessing.py` — Image Preprocessing / معالجة الصور

**What it does / ماذا يفعل:**
Prepares uploaded images for the classifier: loading, resizing, normalization.

```python
def load_image(file_bytes: bytes) -> Image.Image:
    # Load from bytes, convert to RGB

def preprocess_image(image: Image.Image) -> np.ndarray:
    # Resize to 224×224, normalize to [0, 1], add batch dimension
    # Returns shape: (1, 224, 224, 3)
```

#### `app/vision/classifier.py` — Disease Classifier / مصنف الأمراض

**What it does / ماذا يفعل:**
Loads the trained TensorFlow/Keras model and exposes a `predict()` interface. Uses lazy singleton pattern (loads model only once).

```python
class PoultryClassifier:
    def __init__(self, model_path="./models/poultry_classifier.keras"):
        self.class_names = ("Coccidiosis", "Healthy", "New Castle Disease", "Salmonella")

    def predict_proba(self, preprocessed_image) -> np.ndarray:
        # Returns probability for each class
```

**4 Disease Classes / 4 فئات أمراض:**
| Index | Class | Arabic |
|-------|-------|--------|
| 0 | Coccidiosis | الكوكسيديا |
| 1 | Healthy | صحي |
| 2 | New Castle Disease | مرض نيوكاسل |
| 3 | Salmonella | السلمونيلا |

#### `app/vision/predictor.py` — Predictor / المتنبئ

**What it does / ماذا يفعل:**
End-to-end prediction: raw image bytes → preprocessing → classifier → clean result.

```python
@dataclass
class DiagnosisPrediction:
    disease: str
    confidence: float
    all_probabilities: dict  # {class_name: probability}

class Predictor:
    def predict(self, file_bytes: bytes) -> DiagnosisPrediction:
        image = load_image(file_bytes)
        array = preprocess_image(image)
        probs = self.classifier.predict_proba(array)
        best_idx = int(np.argmax(probs))
        return DiagnosisPrediction(...)
```

#### `app/vision/explainer.py` — Diagnosis Explainer / شارح التشخيص

**What it does / ماذا يفعل:**
Bridges the vision pipeline's disease prediction into the RAG pipeline to produce a full, grounded explanation in Egyptian Arabic.

```python
class DiagnosisExplainer:
    def diagnose_and_explain(self, file_bytes: bytes) -> dict:
        # 1. Predict disease from image
        # 2. If confidence < 40%, return warning
        # 3. Use RAG to explain the disease
        # 4. Format in Arabic with structured sections
        return {
            "disease": ...,
            "confidence": ...,
            "explanation": ...,  # Arabic formatted text
            "sources": ...,
            "all_probabilities": ...
        }
```

**Arabic Disease Name Mapping / أسماء الأمراض بالعربية:**
```python
DISEASE_NAME_AR = {
    "Coccidiosis": "الكوكسيديا",
    "Healthy": "صحي",
    "New Castle Disease": "مرض نيوكاسل",
    "Salmonella": "السلمونيلا",
}
```

---

### 3.4 API Module / وحدة API

#### `app/api/chat.py` — Chat Endpoint / نقطة نهاية المحادثة

```python
@router.post("/", response_model=ChatResponse)
def ask_question(payload: ChatRequest) -> ChatResponse:
    # 1. Wait for pipeline warm-up (20s timeout)
    # 2. Call pipeline.answer_question()
    # 3. Log to database
    return ChatResponse(answer=..., sources=...)
```

#### `app/api/image.py` — Image Diagnosis Endpoint / نقطة نهاية تشخيص الصور

```python
@router.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_image(file: UploadFile) -> DiagnosisResponse:
    # 1. Validate file type (must be image/*)
    # 2. Read file bytes
    # 3. Call explainer.diagnose_and_explain()
    # 4. Log to database
    return DiagnosisResponse(disease=..., confidence=..., explanation=..., ...)
```

#### `app/api/upload.py` — PDF Upload Endpoint / نقطة نهاية رفع PDF

**Status: NOT YET IMPLEMENTED / لم يتم التنفيذ بعد**

```python
@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile) -> UploadResponse:
    raise NotImplementedError  # TODO
```

---

### 3.5 Database Module / وحدة قاعدة البيانات

#### `app/database/history.py` — Chat & Diagnosis History / تاريخ المحادثات والتشخيصات

**What it does / ماذا يفعل:**
Lightweight SQLite persistence for chat and diagnosis history.

```python
# Tables:
# - chat_history (id, question, answer, created_at)
# - diagnosis_history (id, disease, confidence, explanation, created_at)

def init_db():        # Create tables if not exist
def log_chat(q, a):   # Insert chat record
def log_diagnosis(disease, confidence, explanation):  # Insert diagnosis record
```

---

### 3.6 Services Module / وحدة الخدمات

#### `app/services/knowledge_base_service.py` — KB Ingestion / إدخال قاعدة المعرفة

**What it does / ماذا يفعل:**
Orchestrates the ingestion flow: load document → clean text → chunk → add to vector store.

```python
class KnowledgeBaseService:
    def ingest_document(self, path) -> int:
        raw_doc = load_document(path)
        cleaned = clean_text(raw_doc.text)
        chunks = chunk_text(cleaned, raw_doc.metadata)
        self.vector_store.add_chunks(chunks)
        return len(chunks)

    def ingest_directory(self, directory="data/pdfs") -> dict:
        # Process all PDFs/DOCXs in directory
        return {"files_processed": ..., "chunks_indexed": ..., "errors": ...}
```

---

### 3.7 Frontend Module / وحدة الواجهة الأمامية

#### `app/streamlit_app.py` — Main Entry Point / نقطة الدخول الرئيسية

Routes to different pages based on sidebar selection:
- Dashboard → `render_dashboard()`
- AI Assistant → `render_assistant()`
- Image Analysis → `render_image_analysis()`
- Disease Library → `render_disease_library()`
- Farm Health / Alerts / Settings → Stubs ("coming soon")

#### `app/components/sidebar.py` — Sidebar Component / مكون الشريط الجانبي

Custom-styled sidebar with:
- Brand header ("🐔 PoultryCare AI")
- Navigation buttons with active state
- System status indicators
- Dark theme with gradient background

#### `app/components/chat.py` — Chat Components / مكونات المحادثة

- `render_chat_message()` — Single chat message
- `render_answer_card()` — Professional answer card with sources and feedback
- `render_suggested_questions()` — Clickable question chips

#### `app/pages/assistant.py` — AI Assistant Page / صفحة المساعد الذكي

- Chat interface with suggested questions
- Calls `/chat/` API endpoint
- Maintains session-based chat history
- Handles quick access queries from dashboard

#### `app/pages/image_analysis.py` — Image Analysis Page / صفحة تحليل الصور

- File upload (JPG/PNG, up to 10MB)
- Calls `/image/diagnose` API endpoint
- Shows prediction, confidence, explanation, all probabilities
- Links to Disease Library and AI Assistant

---

## 4. RAG Pipeline Deep Dive / تحليل معمارية RAG

### 4.1 Document Ingestion Flow / تدفق إدخال المستندات

```
PDF/DOCX File
     │
     ▼
┌──────────────┐
│   Loader     │  ← pypdf or OCR (PyMuPDF + Tesseract)
│  (loader.py) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Preprocessor │  ← Clean noise, normalize Unicode
│(preprocessing│
│    .py)      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Chunker    │  ← Sentence-aware splitting with overlap
│ (chunking.py)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Embedder    │  ← sentence-transformers (384-dim)
│(embeddings.py│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Vector Store │  ← JSON file with cosine similarity
│(vector_store │
│    .py)      │
└──────────────┘
```

### 4.2 Query Flow / تدفق الاستعلام

```
User Question
     │
     ▼
┌──────────────┐
│  Embedder    │  ← Same model as ingestion
│ (embed_query)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Vector Store │  ← Cosine similarity search
│ (similarity  │     Returns top_k=5 candidates
│  _search)    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Reranker   │  ← Cross-encoder re-scoring
│ (reranker.py)│     Returns top_k=3 final chunks
└──────┬───────┘
       │
       ▼
┌──────────────┐
│Prompt Builder│  ← System prompt + context + history
│(prompt_builder│
│    .py)      │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   LLM Call   │  ← OpenRouter API (GPT-4o-mini)
│ (pipeline.py)│     With retry + fallback
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Section    │  ← Extract relevant section based on
│   Extract    │     question keywords
│ (pipeline.py)│
└──────┬───────┘
       │
       ▼
  Arabic Answer
```

### 4.3 Chunking Strategy / استراتيجية التقسيم

**Sentence-Aware Splitting (Primary):**
```python
# Split by sentence boundaries (. ? !)
sentences = re.split(r"(?<=[.?!])\s+", cleaned_text)
# Group sentences until chunk_size is reached
# No overlap at sentence level (natural boundaries)
```

**Word-Based Splitting (Fallback):**
```python
# Split by words
words = re.findall(r"\S+", cleaned_text)
# Slide window: target_words = chunk_size // 8
# Overlap: overlap_words = chunk_overlap // 8
```

**Why sentence-aware? / لماذا التقسيم حسب الجمل؟**
- Preserves semantic完整性
- Avoids cutting mid-sentence
- Better for LLM context consumption

### 4.4 Embedding Model Choice / اختيار نموذج التضمين

| Model | Dimensions | Languages | Size | Speed |
|-------|-----------|-----------|------|-------|
| paraphrase-multilingual-MiniLM-L12-v2 | 384 | 50+ | ~120MB | Fast |
| all-MiniLM-L6-v2 | 382 | English only | ~80MB | Faster |
| multilingual-e5-large | 1024 | 100+ | ~1.1GB | Slow |

**Chosen: paraphrase-multilingual-MiniLM-L12-v2** — Best balance of multilingual support (including Arabic), size, and quality.

### 4.5 Reranking Strategy / استراتيجية إعادة الترتيب

**Why rerank? / لماذا إعادة الترتيب؟**
- Initial retrieval (bi-encoder) is fast but less accurate
- Reranking (cross-encoder) is slower but more accurate
- We rerank only top-k candidates (not all documents) → acceptable latency

**Model: cross-encoder/ms-marco-MiniLM-L-6-v2**
- Trained on MS MARCO dataset
- 6-layer cross-encoder
- Good balance of speed and accuracy

---

## 5. Vision Pipeline Deep Dive / تحليل معمارية الرؤية

### 5.1 Model Architecture / بنية النموذج

```
Input: RGB Image (224 × 224 × 3)
     │
     ▼
┌──────────────────┐
│  Preprocessing   │  ← Resize + Normalize [0,1]
│  (1, 224, 224, 3)│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Keras Model     │  ← Loaded from .keras file
│  (TensorFlow)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Softmax Output  │  ← 4 probabilities (sum = 1)
│  [p0, p1, p2, p3]│
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  argmax(p)       │  ← Highest probability = predicted class
└──────────────────┘
```

### 5.2 Disease Classes / فئات الأمراض

| Index | Disease | Arabic | Description |
|-------|---------|--------|-------------|
| 0 | Coccidiosis | الكوكسيديا | Parasitic disease affecting intestines |
| 1 | Healthy | صحي | No disease detected |
| 2 | New Castle Disease | مرض نيوكاسل | Viral respiratory disease |
| 3 | Salmonella | السلمونيلا | Bacterial infection |

### 5.3 Confidence Threshold / عتبة الثقة

```python
if confidence < 0.4:  # 40%
    # Return warning message instead of full diagnosis
    explanation = "تنبيه: ثقة النموذج منخفضة. النتيجة قد لا تكون دقيقة."
```

**Why 40%? / لماذا 40%؟**
- Below 40%, the model is essentially guessing
- Prevents misleading farmers with low-confidence diagnoses
- Still returns the prediction for reference

---

## 6. Database Design / تصميم قاعدة البيانات

### 6.1 Schema / المخطط

```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TEXT NOT NULL  -- ISO 8601 format (UTC)
);

CREATE TABLE diagnosis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disease TEXT NOT NULL,
    confidence REAL NOT NULL,
    explanation TEXT NOT NULL,
    created_at TEXT NOT NULL  -- ISO 8601 format (UTC)
);
```

### 6.2 Design Decisions / قرارات التصميم

| Decision | Rationale |
|----------|-----------|
| SQLite | Simple, no server needed, sufficient for single-user |
| UTC timestamps | Avoids timezone confusion |
| TEXT for created_at | ISO 8601 is sortable and human-readable |
| Separate tables | Chat and diagnosis are different entities |
| No foreign keys | Simplifies schema, history is append-only |

---

## 7. API Design / تصميم واجهة البرمجة

### 7.1 Endpoints / نقاط النهاية

| Method | Path | Request | Response | Status |
|--------|------|---------|----------|--------|
| POST | `/chat/` | `{question, session_id?}` | `{answer, sources}` | ✅ Implemented |
| POST | `/image/diagnose` | `file: UploadFile` | `{disease, confidence, explanation, sources, all_probabilities}` | ✅ Implemented |
| POST | `/upload/pdf` | `file: UploadFile` | `{filename, chunks_indexed}` | ❌ Not implemented |
| GET | `/health` | — | `{status: "ok"}` | ✅ Implemented |
| GET | `/` | — | Redirect to `/docs` | ✅ Implemented |

### 7.2 Request/Response Models / نماذج الطلب والاستجابة

```python
# Chat
class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]

# Image Diagnosis
class DiagnosisResponse(BaseModel):
    disease: str
    confidence: float
    explanation: str
    sources: list[dict]
    all_probabilities: dict
```

---

## 8. Frontend (Streamlit) / الواجهة الأمامية

### 8.1 Pages / الصفحات

| Page | File | Description |
|------|------|-------------|
| Dashboard | `pages/dashboard.py` | Hero section, quick access, features |
| AI Assistant | `pages/assistant.py` | Chat interface with suggested questions |
| Image Analysis | `pages/image_analysis.py` | Upload + diagnosis results |
| Disease Library | `pages/disease_library.py` | Browsable disease categories |
| Farm Health | — | Stub ("coming soon") |
| Alerts | — | Stub ("coming soon") |
| Settings | — | Stub ("coming soon") |
| About | — | Project description |

### 8.2 Communication Pattern / نمط الاتصال

```
Streamlit Frontend (port 8501)
        │
        │ HTTP POST (requests library)
        ▼
FastAPI Backend (port 8001)
        │
        │ Returns JSON
        ▼
Streamlit renders response
```

**Why separate processes? / لماذا عمليات منفصلة؟**
- Streamlit and FastAPI have different runtime models
- Allows independent scaling
- Cleaner separation of concerns
- Can replace frontend without touching backend

---

## 9. Important Comparisons / مقارنات مهمة

### 9.1 Vector Store: JSON vs ChromaDB vs FAISS

| Aspect | JSON (Used) | ChromaDB | FAISS |
|--------|-------------|----------|-------|
| Setup | None | Server/Embedded | Library |
| Dependencies | None | chromadb | faiss-cpu |
| Persistence | File-based | File/Server | File |
| Scalability | Small (<10K chunks) | Medium | Large |
| Similarity | Cosine (manual) | Built-in | Built-in |
| Debugging | Easy (read JSON) | Harder | Harder |
| Best For | Prototyping | Production | Large-scale |

**Why JSON was chosen / لماذا تم اختيار JSON:**
- Simple deployment, no additional dependencies
- Easy to inspect and debug
- Sufficient for the project's knowledge base size

### 9.2 Embedding Models Comparison / مقارنة نماذج التضمين

| Model | Dims | Arabic | Size | Quality |
|-------|------|--------|------|---------|
| paraphrase-multilingual-MiniLM-L12-v2 ✅ | 384 | ✅ | 120MB | Good |
| all-MiniLM-L6-v2 | 382 | ❌ | 80MB | Good (EN) |
| multilingual-e5-large | 1024 | ✅ | 1.1GB | Best |
| text-embedding-ada-002 | 1536 | ✅ | API | Best |

### 9.3 LLM Providers Comparison / مقارنة مزودي النماذج اللغوية

| Provider | Model | Cost | Latency | Quality |
|----------|-------|------|---------|---------|
| OpenRouter ✅ | GPT-4o-mini | Low | Fast | Good |
| OpenAI Direct | GPT-4o | Medium | Medium | Best |
| Google | Gemini Pro | Low | Fast | Good |
| Local (Ollama) | Llama 3 | Free | Slow | Medium |

### 9.4 Reranking Approaches / مقارنة طرق إعادة الترتيب

| Approach | Speed | Quality | Used? |
|----------|-------|---------|-------|
| No reranking | Fastest | Lowest | ❌ |
| BM25 (lexical) | Fast | Medium | ❌ |
| Cross-encoder ✅ | Slow | Highest | ✅ |
| ColBERT | Medium | High | ❌ |

### 9.5 OCR Approaches / مقارنة طرق التعرف الضوئي

| Approach | Arabic | Speed | Quality |
|----------|--------|-------|---------|
| Tesseract ✅ | ✅ | Medium | Good |
| EasyOCR | ✅ | Slow | Good |
| PaddleOCR | ✅ | Fast | Best |
| Google Vision API | ✅ | Fast | Best (paid) |

---

## 10. Identified Bugs & Fixes / الأخطاء المكتشفة والحلول

### Bug 1: `.env` File Contains Real API Key / ملف `.env` يحتوي على مفتاح API حقيقي

**File:** `.env` (line 1)

**Problem / المشكلة:**
```python
OPENROUTER_API_KEY=<redacted_openrouter_api_key>
```
A real API key is hardcoded in the `.env` file, which is a security risk if the repository is shared.

مفتاح API حقيقي موجود في ملف `.env`، وهو خطر أمني إذا تم مشاركة المستودع.

**Fix / الحل:**
```python
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
Replace with placeholder. Add `.env` to `.gitignore`.

---

### Bug 2: `upload.py` Not Implemented / `upload.py` غير منفذ

**File:** `app/api/upload.py` (line 35)

**Problem / المشكلة:**
```python
@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    raise NotImplementedError
```
The PDF upload endpoint raises `NotImplementedError`, which returns a 500 error to the client.

**Fix / الحل:**
Implement the endpoint using `KnowledgeBaseService`:
```python
@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files are accepted.")
    saved_path = Path("data/pdfs") / file.filename
    ensure_dir(saved_path.parent)
    saved_path.write_bytes(await file.read())
    service = KnowledgeBaseService()
    chunks = service.ingest_document(saved_path)
    return UploadResponse(filename=file.filename, chunks_indexed=chunks)
```

---

### Bug 3: `_extract_relevant_section` May Return Too Little Text / قد يُرجع النص قليلاً جداً

**File:** `app/rag/pipeline.py` (line 64)

**Problem / المشكلة:**
```python
if len(section_content) < 50:
    return section_content  # Returns very short content
```
If a section has less than 50 characters, it's returned as-is, which may be too short to be useful.

**Fix / الحل:**
```python
if len(section_content) < 50:
    # Return full text instead of truncated section
    return text
```

---

### Bug 4: No Input Validation on Chat Request / لا يوجد تحقق من المدخلات

**File:** `app/api/chat.py`

**Problem / المشكلة:**
The `ChatRequest` model accepts any string, including empty strings, which could cause issues downstream.

**Fix / الحل:**
```python
class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

    @validator('question')
    def question_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty')
        return v.strip()
```

---

### Bug 5: Thread Safety Issue in Pipeline Warm-up / مشكلة أمان الخيوط في التسخين

**File:** `app/main.py` (line 22-37)

**Problem / المشكلة:**
```python
def warm_up_rag() -> None:
    pipeline = RAGPipeline()
    pipeline.answer_question("test warm up query", session_id="warmup_session")
    state.pipeline = pipeline  # Race condition possible
```
The `state.pipeline` assignment could race with requests that check `state.pipeline_ready`.

**Current Mitigation / الحل الحالي:**
Uses `threading.Event` (`pipeline_ready`) to synchronize. The `get_pipeline()` function in `chat.py` waits for the event before accessing the pipeline. This is sufficient for the current use case.

---

### Bug 6: Conversation Memory Not Persisted / ذاكرة المحادثة غير محفوظة

**File:** `app/rag/pipeline.py`

**Problem / المشكلة:**
`ConversationMemory` stores history in-memory only. If the server restarts, all conversation history is lost.

**Impact / التأثير:**
- Low — conversations are short-lived anyway
- Database logs persist separately

**Potential Fix / حل محتمل:**
Store conversation turns in SQLite alongside the existing `chat_history` table, keyed by `session_id`.

---

### Bug 7: `_clean_extracted_page_text` Duplicate Logic / منطق مكرر

**File:** `app/rag/loader.py` (line 45-67) vs `app/rag/preprocessing.py`

**Problem / المشكلة:**
The `_clean_extracted_page_text` function in `loader.py` duplicates some cleaning logic that already exists in `preprocessing.py` (e.g., `remove_boilerplate`, duplicate sentence removal).

**Fix / الحل:**
Refactor to use `preprocessing.clean_text()` directly, or extract shared logic into a common utility.

---

### Bug 8: Hardcoded API URL in Frontend / رابط API ثابت في الواجهة

**File:** `app/pages/assistant.py` (line 13)

**Problem / المشكلة:**
```python
API_BASE_URL = "http://localhost:8001"
```
Hardcoded URL won't work in production or different environments.

**Fix / الحل:**
```python
import os
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8001")
```

---

### Bug 9: No Rate Limiting on API Endpoints / لا يوجد حد للطلبات

**File:** `app/main.py`

**Problem / المشكلة:**
No rate limiting on any endpoint. A malicious client could overwhelm the server.

**Fix / الحل:**
Add `slowapi` or similar rate limiting middleware:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

### Bug 10: `Translator` Class Not Used / فئة `Translator` غير مستخدمة

**File:** `app/core/utils.py` (line 54-79)

**Problem / المشكلة:**
The `Translator` class is defined but never imported or used anywhere in the codebase.

**Fix / الحل:**
Either use it in the pipeline for English-to-Arabic translation, or remove it to reduce dead code.

---

## 11. 25 Professor Questions & Answers / 25 سؤال من المُحاضر مع الإجابات

### Q1: What is RAG and why did you use it? / ما هو RAG ولماذا استخدمته؟

**Answer / الإجابة:**
RAG (Retrieval-Augmented Generation) is a technique that combines information retrieval with language generation. Instead of relying solely on the LLM's training data, we first retrieve relevant documents from a knowledge base, then provide them as context to the LLM.

We used RAG because:
1. **Domain-specific knowledge** — Poultry disease information isn't well-covered in general LLM training data
2. **Updatable** — We can add new documents without retraining the model
3. **Grounded answers** — Responses are based on actual veterinary documents, reducing hallucination
4. **Source attribution** — We can show users which documents informed the answer

RAG (الاسترجاع المعزز بالتوليد) هو تقنية تجمع بين استرجاع المعلومات وتوليد اللغة. بدلاً من الاعتماد فقط على بيانات تدريب النموذج اللغوي، نسترجع أولاً المستندات ذات الصلة من قاعدة المعرفة، ثم نقدمها كسياق للنموذج اللغوي.

---

### Q2: Explain the difference between bi-encoder and cross-encoder. / اشرح الفرق بين المرمز الثنائي والمرمز المتقاطع

**Answer / الإجابة:**
| Aspect | Bi-Encoder | Cross-Encoder |
|--------|-----------|---------------|
| Input | Query and document separately | Query and document together |
| Speed | Fast (can pre-compute) | Slow (must compute per pair) |
| Quality | Lower (independent encoding) | Higher (joint attention) |
| Use Case | Initial retrieval (top-k from millions) | Reranking (top-k from dozens) |

In our system:
- **Bi-encoder** (`sentence-transformers`): Used in `EmbeddingModel` for initial retrieval from the vector store
- **Cross-encoder** (`CrossEncoder`): Used in `Reranker` to re-score the top candidates

---

### Q3: Why did you choose JSON over ChromaDB for the vector store? / لماذا اخترت JSON بدلاً من ChromaDB؟

**Answer / الإجابة:**
1. **Simplicity** — No additional server or dependency needed
2. **Debugging** — Can inspect the JSON file directly
3. **Sufficient scale** — Our knowledge base is small (< 1000 chunks)
4. **Portability** — Works anywhere Python runs
5. **No configuration** — No database setup required

For production with larger knowledge bases, I would switch to ChromaDB or FAISS.

---

### Q4: How does the OCR fallback work? / كيف يعمل البديل OCR؟

**Answer / الإجابة:**
```
1. Try pypdf first (fast, clean text extraction)
2. If extracted text < 500 characters:
   a. Open PDF with PyMuPDF (fitz)
   b. Render each page as image (300 DPI)
   c. Run Tesseract OCR (Arabic + English)
   d. Clean extracted text
   e. Use OCR text if longer than pypdf text
```

This handles scanned PDFs where pypdf can't extract text (no text layer).

---

### Q5: What is the chunking strategy and why? / ما هي استراتيجية التقسيم ولماذا؟

**Answer / الإجابة:**
We use **sentence-aware splitting** as the primary strategy:
- Split text by sentence boundaries (`.`, `?`, `!`)
- Group sentences until `chunk_size` (450 chars ÷ 8 ≈ 56 words) is reached
- Natural boundaries preserve semantic完整性

Fallback: **word-based sliding window** with overlap for texts without clear sentence boundaries.

**Why sentence-aware?**
- Preserves complete thoughts
- Better for LLM context consumption
- Avoids mid-sentence cuts that lose meaning

---

### Q6: Explain the conversation memory mechanism. / اشرح آلية ذاكرة المحادثة

**Answer / الإجابة:**
```python
class ConversationMemory:
    _history: dict[str, list[dict]]  # session_id → list of {question, answer}
    _max_turns = 10                  # Keep last 10 turns per session
```

- Each session has a unique `session_id` (UUID)
- When answering, we include the last 6 turns as context
- This allows follow-up questions like "What about treatment?" to work
- History is in-memory only (lost on restart)
- Database stores a separate persistent log

---

### Q7: How do you handle LLM failures? / كيف تتعامل مع فشل النموذج اللغوي؟

**Answer / الإجابة:**
Three-layer strategy:

1. **Retry with backoff** — Up to 3 retries for transient errors (rate limit, timeout, server errors)
   ```python
   wait = 1.0 * (2 ** attempt)  # 1s, 2s, 4s
   ```

2. **Error classification** — Check if error message matches known transient patterns

3. **Graceful fallback** — If all retries fail, return raw retrieved context with a message:
   ```
   "الذكاء الاصطناعي غير متاح مؤقتاً. إليك المعلومات الأكثر صلة من قاعدة المعرفة"
   ```

---

### Q8: What is the confidence threshold for image diagnosis? / ما هي عتبة الثقة لتشخيص الصور؟

**Answer / الإجابة:**
**40% (0.4)**

If the classifier's confidence is below 40%:
- We return a warning message instead of a full diagnosis
- The warning says: "تنبيه: ثقة النموذج منخفضة. النتيجة قد لا تكون دقيقة."
- We still return the prediction for reference
- We recommend consulting a veterinarian

**Why 40%?**
- With 4 classes, random chance is 25%
- 40% is above random but still uncertain
- Prevents misleading farmers with low-confidence diagnoses

---

### Q9: How does the system handle Arabic text? / كيف يتعامل النظام مع النص العربي؟

**Answer / الإجابة:**
Multiple layers:

1. **Embedding model** — `paraphrase-multilingual-MiniLM-L12-v2` supports Arabic natively
2. **OCR** — Tesseract configured with `lang="ara+eng"` for Arabic + English
3. **Preprocessing** — Arabic-specific noise patterns (PDF artifacts, repeated text)
4. **Normalization** — Maps variant Arabic spellings to canonical forms
5. **Prompts** — All system prompts in Egyptian Arabic dialect
6. **Output** — Structured with Arabic emoji headers (🐔, 🦠, 🔍, 💊, 🛡️)

---

### Q10: What is the purpose of the reranker? / ما هو الغرض من إعادة الترتيب؟

**Answer / الإجابة:**
The reranker improves retrieval precision by:
1. Taking the top-k candidates from the initial bi-encoder search
2. Re-scoring them using a cross-encoder that sees query + document together
3. Returning the top-k most relevant after re-scoring

**Without reranker:** Top results might be semantically similar but not actually relevant
**With reranker:** Results are more precisely matched to the query intent

Trade-off: Adds ~100-200ms latency, but significantly improves answer quality.

---

### Q11: Explain the project's directory structure. / اشرح هيكل مجلدات المشروع

**Answer / الإجابة:**
```
app/
├── api/            # FastAPI route handlers (chat, image, upload)
├── rag/            # RAG pipeline (loader, preprocessing, chunking,
│                   #   embeddings, vector_store, retriever, reranker,
│                   #   prompt_builder, pipeline)
├── vision/         # Image classification (preprocessing, classifier,
│                   #   predictor, explainer)
├── services/       # Cross-cutting services (knowledge_base_service)
├── database/       # SQLite persistence (history)
├── core/           # Config, logging, utilities
├── components/     # Streamlit UI components (sidebar, header, chat)
├── pages/          # Streamlit pages (dashboard, assistant, etc.)
├── streamlit_app.py # Streamlit entry point
└── main.py         # FastAPI entry point
```

---

### Q12: How is the system secured? / كيف يتم تأمين النظام؟

**Answer / الإجابة:**
1. **API keys** — Never hardcoded; loaded from `.env` or Streamlit secrets
2. **`.gitignore`** — Excludes `.env` and `secrets.toml`
3. **CORS** — Currently allows all origins (should be restricted in production)
4. **Input validation** — File type checking for image uploads
5. **No authentication** — Currently no user auth (acceptable for prototype)

**Production recommendations:**
- Add API key authentication
- Restrict CORS origins
- Add rate limiting
- Add input sanitization

---

### Q13: What is the warm-up mechanism? / ما هي آلية التسخين؟

**Answer / الإجابة:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Initialize database tables
    init_db()
    # 2. Start RAG warm-up in background thread
    warmup_thread = threading.Thread(target=warm_up_rag, daemon=True)
    warmup_thread.start()
    yield

def warm_up_rag():
    # 1. Create RAGPipeline (loads embedding model, connects to vector store)
    pipeline = RAGPipeline()
    # 2. Run a test query to compile/cache tokenizers
    pipeline.answer_question("test warm up query", session_id="warmup_session")
    # 3. Store in global state
    state.pipeline = pipeline
    # 4. Signal ready
    state.pipeline_ready.set()
```

**Why background thread?**
- Doesn't block server startup
- Server can respond to `/health` immediately
- First real request waits for warm-up (20s timeout)

---

### Q14: How does the section extraction work? / كيف تعمل استخراج الأقسام؟

**Answer / الإجابة:**
After the LLM generates a full diagnosis, we extract only the relevant section based on the user's question:

```python
def _extract_relevant_section(text, question):
    # Detect question type by Arabic keywords:
    if 'سبب' in question:     → Extract "🦠 الأسباب:" section
    if 'أعراض' in question:   → Extract "🔍 الأعراض:" section
    if 'علاج' in question:    → Extract "💊 العلاج:" section
    if 'وقاية' in question:   → Extract "🛡️ الوقاية:" section
    else:                     → Return full text
```

This provides focused answers instead of dumping the entire diagnosis.

---

### Q15: What are the limitations of the current system? / ما هي قيود النظام الحالي؟

**Answer / الإجابة:**
1. **Small knowledge base** — Only a few PDFs indexed
2. **No authentication** — Anyone can access the API
3. **In-memory conversation** — Lost on server restart
4. **Single-user design** — No multi-tenant support
5. **No real-time updates** — Must re-index manually
6. **Limited disease classes** — Only 4 classes in the vision model
7. **No feedback loop** — Can't learn from user corrections
8. **JSON vector store** — Won't scale to large knowledge bases
9. **No caching layer** — No Redis/Memcached for frequent queries
10. **Basic error handling** — Could be more granular

---

### Q16: How would you scale this system? / كيف توسع هذا النظام؟

**Answer / الإجابة:**
1. **Vector store** — Switch to ChromaDB/Pinecone/Weaviate
2. **Database** — Switch to PostgreSQL
3. **Caching** — Add Redis for query caching
4. **Authentication** — Add JWT-based auth
5. **Rate limiting** — Add slowapi or API gateway
6. **Containerization** — Docker + Kubernetes
7. **Load balancing** — Multiple FastAPI instances
8. **Async processing** — Celery for document ingestion
9. **Monitoring** — Prometheus + Grafana
10. **CI/CD** — Automated testing and deployment

---

### Q17: Explain the retry mechanism. / اشرح آلية إعادة المحاولة

**Answer / الإجابة:**
```python
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 1.0  # seconds

for attempt in range(MAX_RETRIES):
    try:
        completion = client.chat.completions.create(...)
        return completion.choices[0].message.content
    except Exception as exc:
        if _is_transient_error(exc) and attempt < MAX_RETRIES - 1:
            wait = RETRY_BACKOFF_BASE * (2 ** attempt)  # 1s, 2s, 4s
            time.sleep(wait)
        else:
            break  # Fall back to raw context
```

**Transient errors:** rate limit, timeout, service unavailable, internal server error, bad gateway, gateway timeout

**Non-transient errors:** invalid API key, model not found → immediate fallback

---

### Q18: How does the query cache work? / كيف يعمل ذاكرة الاستعلام المؤقتة؟

**Answer / الإجابة:**
```python
class RAGPipeline:
    _query_cache: dict[str, tuple[list[dict], ...]] = {}

    def _get_cached_or_compute(self, query):
        cache_key = query.strip().lower()
        if cache_key in self._query_cache:
            return list(self._query_cache[cache_key])
        candidates = self.retriever.retrieve(query)
        top_chunks = self.reranker.rerank(query, candidates)
        self._query_cache[cache_key] = tuple(top_chunks)
        return top_chunks
```

- Cache key: normalized query (lowercase, stripped)
- Cache value: tuple of retrieved + reranked chunks
- Avoids re-computing embeddings and similarity search for repeated queries
- In-memory only (cleared on restart)

---

### Q19: What is the role of `state.py`? / ما هو دور `state.py`؟

**Answer / الإجابة:**
```python
class AppState:
    def __init__(self):
        self.pipeline = None                    # RAGPipeline instance
        self.pipeline_ready = threading.Event()  # Synchronization primitive

state = AppState()  # Global singleton
```

**Purpose:**
- Stores the warmed-up RAG pipeline instance
- `pipeline_ready` event synchronizes startup:
  - Background thread sets it when warm-up completes
  - API handlers wait on it before processing requests
- Thread-safe communication between warm-up thread and request handlers

---

### Q20: How does the Explainer format Arabic output? / كيف يُنسق الشرح النص العربي؟

**Answer / الإجابة:**
The `DiagnosisExplainer._build_arabic_explanation()` method:

1. **Healthy path** — Short format:
   ```
   🐔 تشخيص المرض: صحي بثقة 95%.
   ⚠️ يُرجى تأكيد التشخيص بواسطة طبيب بيطري.
   ```

2. **Disease path** — Full format:
   ```
   🐔 تشخيص المرض: الكوكسيديا بثقة 87%.
   ⚠️ يُرجى تأكيد التشخيص بواسطة طبيب بيطري.

   🦠 الأسباب:
   - سبب 1
   - سبب 2

   🔍 الأعراض:
   - عرض 1
   - عرض 2

   💊 العلاج:
   - علاج 1
   - علاج 2

   🛡️ الوقاية:
   - وقاية 1

   📌 ملاحظة:
   النتيجة دي معمولة بالذكاء الاصطناعي بهدف المساعدة، لكنها ما تغنيش عن تشخيص الطبيب البيطري.
   ```

3. **Parsing** — Tries JSON first, falls back to keyword-based paragraph classification

---

### Q21: What testing is in place? / ما هي الاختبارات الموجودة؟

**Answer / الإجابة:**
Two test files:

**`test_rag_pipeline.py` (6 tests):**
1. `test_clean_text_normalizes_hyphenated_line_breaks` — Text preprocessing
2. `test_chunk_text_returns_overlapping_chunks` — Chunking logic
3. `test_embedding_model_returns_vectors` — Embedding generation
4. `test_vector_store_round_trip` — Store + retrieve
5. `test_pipeline_returns_answer_and_sources` — Full pipeline
6. `test_fallback_uses_retrieved_context_when_llm_is_unavailable` — Graceful degradation

**`test_database.py` (3 tests):**
1. `test_init_db_creates_tables` — Schema creation
2. `test_log_chat_inserts_record` — Chat logging
3. `test_log_diagnosis_inserts_record` — Diagnosis logging

---

### Q22: How does the system handle different file formats? / كيف يتعامل النظام مع صيغ الملفات المختلفة؟

**Answer / الإجابة:**
```python
def load_document(path) -> RawDocument | None:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)      # pypdf → OCR fallback
    if suffix == ".docx":
        return load_docx(path)     # python-docx
    return None                    # Unsupported format
```

**PDF handling:**
1. Try `pypdf` (fast, clean text)
2. If < 500 chars, try OCR (PyMuPDF + Tesseract)

**DOCX handling:**
1. Extract paragraphs
2. Extract tables (pipe-separated cells)

**Unsupported:** Returns `None`, logged as warning

---

### Q23: What is the purpose of `normalizer.py`? / ما هو الغرض من `normalizer.py`؟

**Answer / الإجابة:**
Normalizes Arabic text by mapping variant spellings to canonical forms:

```python
_VARIANT_MAP = {
    "نيوكاسيل": "نيوكاسل",      # Common misspelling
    "النيوكاسيل": "النيوكاسل",   # With article
    "اتش بي": "ايب",            # H.P. → IB (Infectious Bronchitis)
}
```

**Why?**
- Users may type disease names differently
- Arabic has many spelling variants
- Normalization improves retrieval accuracy
- Maps colloquial terms to standard veterinary terms

---

### Q24: Explain the lifespan context manager. / اشرح مدير سياق lifespan

**Answer / الإجابة:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP:
    # 1. Initialize database
    init_db()
    # 2. Start RAG warm-up in background
    warmup_thread = threading.Thread(target=warm_up_rag, daemon=True)
    warmup_thread.start()

    yield  # Server is running, accepting requests

    # SHUTDOWN:
    # (Nothing to clean up currently)
```

**Why `asynccontextmanager`?**
- FastAPI's recommended way to handle startup/shutdown
- Code before `yield` runs on startup
- Code after `yield` runs on shutdown
- `daemon=True` ensures warm-up thread dies with the main process

---

### Q25: How would you improve this project? / كيف تحسين هذا المشروع؟

**Answer / الإجابة:**

**Short-term (1-2 weeks):**
1. Implement the `/upload/pdf` endpoint
2. Add input validation (empty questions, file size limits)
3. Add API authentication (API keys or JWT)
4. Fix hardcoded API URLs in frontend
5. Add more comprehensive tests

**Medium-term (1-2 months):**
1. Switch to ChromaDB for vector storage
2. Add Redis caching for frequent queries
3. Implement conversation persistence in SQLite
4. Add rate limiting
5. Add monitoring and logging (structured logs)

**Long-term (3-6 months):**
1. Add more disease classes to the vision model
2. Implement user feedback loop (learn from corrections)
3. Add multi-language support (English interface)
4. Deploy with Docker + Kubernetes
5. Add real-time document ingestion (watch folder)
6. Implement A/B testing for different prompts

---

## 12. Viva Cheat Sheet / ورقة غش المناقشة

### Key Numbers to Remember / أرقام مهمة للتذكر

| Item | Value |
|------|-------|
| Embedding dimensions | 384 |
| Image input size | 224 × 224 × 3 |
| Number of disease classes | 4 |
| Default chunk size | 450 characters |
| Default chunk overlap | 200 characters |
| Retriever top_k | 5 |
| Reranker top_k | 3 |
| Max conversation turns | 10 |
| History turns in prompt | 6 |
| Confidence threshold | 40% |
| Max retries | 3 |
| Retry backoff | 1s, 2s, 4s |
| Warm-up timeout | 20 seconds |
| OCR DPI | 300 |

### One-Line Explanations / شرح في سطر واحد

| Concept | One-liner |
|---------|-----------|
| RAG | Retrieve relevant docs → feed to LLM → grounded answer |
| Bi-encoder | Encodes query & doc independently → fast retrieval |
| Cross-encoder | Encodes query+doc together → accurate reranking |
| Chunking | Split text into overlapping pieces for embedding |
| Cosine similarity | Measures angle between vectors → semantic similarity |
| Warm-up | Pre-load models in background so first request is fast |
| Graceful degradation | If LLM fails, return raw retrieved context |
| Conversation memory | Keep last 10 turns for context-aware answers |
| OCR fallback | If pypdf fails, render pages as images and OCR them |
| Section extraction | Extract only the relevant part of the diagnosis |

### Architecture in 30 Seconds / البنية في 30 ثانية

```
User → Streamlit → FastAPI → RAGPipeline
                                ├── Retriever (bi-encoder search)
                                ├── Reranker (cross-encoder re-score)
                                ├── PromptBuilder (Arabic prompts)
                                └── LLM (OpenRouter/GPT-4o-mini)
                             → Response
```

### Common Professor Traps / مصائد المحاضر الشائعة

| Trap | Correct Answer |
|------|---------------|
| "Why not use GPT-4 directly?" | Cost, latency, and we need domain-specific context (RAG) |
| "Why not use ChromaDB?" | JSON is simpler for prototype; would switch for production |
| "Why Egyptian Arabic?" | Target audience is Egyptian farmers; MSA would feel formal |
| "Why 40% threshold?" | Above random (25%) but still uncertain; prevents misleading |
| "Why rerank at all?" | Bi-encoder is fast but imprecise; cross-encoder catches nuances |
| "Why not fine-tune the LLM?" | RAG is cheaper, updatable, and provides source attribution |
| "Why sentence-aware chunking?" | Preserves semantic完整性; avoids mid-sentence cuts |
| "Why multilingual embeddings?" | Knowledge base has Arabic + English content |

### File Quick Reference / مرجع سريع للملفات

| File | Purpose | Lines |
|------|---------|-------|
| `config.py` | All settings in one place | ~90 |
| `loader.py` | PDF/DOCX loading + OCR | ~230 |
| `preprocessing.py` | Text cleaning | ~150 |
| `chunking.py` | Text splitting | ~90 |
| `embeddings.py` | Sentence-transformers wrapper | ~50 |
| `vector_store.py` | JSON vector store | ~95 |
| `retriever.py` | Semantic search | ~35 |
| `reranker.py` | Cross-encoder reranking | ~60 |
| `prompt_builder.py` | Arabic prompts | ~170 |
| `pipeline.py` | Full RAG orchestration | ~250 |
| `classifier.py` | TF model loader | ~40 |
| `predictor.py` | Image → prediction | ~35 |
| `explainer.py` | Vision → RAG bridge | ~180 |
| `history.py` | SQLite persistence | ~90 |
| `main.py` | FastAPI entry point | ~90 |
| `streamlit_app.py` | Streamlit entry point | ~120 |

---

## 📝 Final Notes / ملاحظات ختامية

### Project Strengths / نقاط قوة المشروع
1. Clean separation of concerns (RAG, Vision, API, Frontend)
2. Comprehensive Arabic support (prompts, OCR, normalization)
3. Graceful degradation (fallback when LLM fails)
4. Good error handling (retry with backoff)
5. Professional UI with dark theme
6. Well-documented code with docstrings

### Project Weaknesses / نقاط ضعف المشروع
1. No authentication/authorization
2. JSON vector store (won't scale)
3. In-memory conversation (lost on restart)
4. Limited test coverage
5. No CI/CD pipeline
6. Hardcoded URLs in frontend

### Future Improvements / تحسينات مستقبلية
1. Add JWT authentication
2. Switch to ChromaDB/Pinecone
3. Add Redis caching
4. Implement Docker deployment
5. Add comprehensive test suite
6. Add monitoring and alerting
7. Support more disease classes
8. Add user feedback mechanism

---

**Document Version:** 1.0
**Date:** 2026-08-27
**Project:** Poultry Disease RAG System
**Author:** Project Documentation Team

---

> ⚠️ **Disclaimer / تنبيه:** This documentation is for educational and viva preparation purposes. The AI system provides informational support and does not replace professional veterinary diagnosis.
>
> ⚠️ **تنبيه:** هذا التوثيق لأغراض التعليم والتحضير للمناقشة. يوفر النظام الدعم المعلوماتي ولا يحل محل التشخيص البيطري المهني.
