# Poultry Disease RAG System

An AI-powered assistant for poultry farmers, veterinarians, and agricultural
specialists that combines:

1. **Question Answering (RAG)** — answers natural-language questions using a
   knowledge base of poultry disease PDFs, retrieved semantically via ChromaDB
   and answered by an LLM (via OpenRouter).
2. **Image-Based Disease Diagnosis** — a deep learning classifier predicts the
   most likely disease from an uploaded poultry image, and the RAG pipeline
   then explains symptoms, causes, treatment, and prevention for that disease.

## Stack
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **Vector DB:** ChromaDB
- **LLM:** OpenRouter (default: `openai/gpt-4o-mini`)
- **Vision model:** Keras/TensorFlow image classifier

## Project Structure
```
app/
├── api/            # FastAPI route handlers
│   ├── chat.py
│   ├── image.py
│   └── upload.py
├── rag/            # Retrieval-Augmented Generation pipeline
│   ├── loader.py
│   ├── preprocessing.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── reranker.py
│   ├── prompt_builder.py
│   └── pipeline.py
├── vision/         # Image classification pipeline
│   ├── preprocessing.py
│   ├── classifier.py
│   ├── predictor.py
│   └── explainer.py
├── services/       # Cross-cutting orchestration services
├── database/       # Persistence (chat history, uploads metadata, etc.)
├── core/           # Config, logging, shared utilities
│   ├── config.py
│   ├── logger.py
│   └── utils.py
├── streamlit_app.py
└── main.py
requirements.txt
.streamlit/secrets.toml   # NOT committed — see .gitignore
models/                    # trained .keras model goes here
data/pdfs/                 # source PDF knowledge base
```

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill
   in your real keys (never commit this file — it's already in `.gitignore`).

3. Place your poultry disease PDF documents in `data/pdfs/`.

4. Place your trained classifier at the path set by `MODEL_PATH` in secrets
   (default: `./models/poultry_classifier.keras`).

5. Run the FastAPI backend:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Run the Streamlit frontend (in a separate terminal):
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Security
- API keys are never hardcoded — they're loaded at runtime from Streamlit
  Secrets (`st.secrets`) via `app/core/config.py`.
- `.env` and `.streamlit/secrets.toml` are excluded from version control.

## Status
This is a scaffolded skeleton. Each module below contains a docstring, a
`# TODO` outline of what it needs to do, and function/class signatures ready
to be implemented.
