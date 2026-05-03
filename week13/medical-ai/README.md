# AI Medical Assistant

Medical RAG assistant powered by AWS Bedrock and Llama 3.

## Project Structure

MEDICAL-AI/
│── app/
│   ├── config.py       # Configuration and Env loading
│   ├── main.py         # FastAPI routes
│── services/
│   ├── document_loader.py # PDF processing
│   ├── embeddings.py      # Bedrock Embeddings
│   ├── llm.py             # Bedrock LLM
│   ├── vector_store.py    # FAISS logic
│   ├── rag_pipeline.py    # RAG orchestration
│── ui/
│   ├── streamlit_app.py   # Streamlit interface
│── .env                   # AWS Credentials
│── data/                  # Uploaded documents
│── faiss_index/           # Local vector database

## Installation

This project is part of a Poetry workspace.
1. Configure `.env` with AWS and Bedrock settings.
2. Ensure dependencies are installed via `poetry install` in root.

## Running the App

### 1. Start Backend (FastAPI)
```bash
poetry run uvicorn app.main:app --reload
```

### 2. Start Frontend (Streamlit)
```bash
poetry run streamlit run ui/streamlit_app.py
```
