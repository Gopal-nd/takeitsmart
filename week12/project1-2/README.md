# Unified RAG Chatbot (FAISS & Pinecone)

A modular RAG application that supports both local (FAISS) and cloud (Pinecone) vector stores.

## Project Structure

PROJECT1-2/
│── app/
│   ├── config.py       # Configuration and Env loading
│── services/
│   ├── embeddings.py    # SentenceTransformer model
│   ├── ingestion.py     # Document loading (TXT)
│   ├── vector_store.py  # FAISS & Pinecone logic
│   ├── llm.py           # Groq Llama 3 integration
│── ui/
│   ├── streamlit_app.py # Unified Streamlit interface
│── data/                # Sample documents

## Features
- **Toggle Vector Stores**: Choose between FAISS (runs locally) or Pinecone (cloud-based) in the sidebar.
- **Persistent Logic**: Modular design allows easy extension (e.g., adding more models or document types).
- **Caching**: Uses Streamlit caching for fast model loading and efficient querying.

## Installation

1. Configure `.env` in the root:
   - `GROQ_API_KEY`
   - `PINECONE_API_KEY` (Optional, required for Pinecone mode)
   - `PINECONE_INDEX_NAME` (Optional)

2. Run the application:
```bash
poetry run streamlit run ui/streamlit_app.py
```
