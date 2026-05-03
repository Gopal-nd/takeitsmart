# Enterprise Multi-Doc RAG System

A modular RAG application for large-scale knowledge retrieval across multiple sources.

## Features
- **Multi-Source Ingestion**:
    - **Files**: PDF, DOCX, CSV, TXT.
    - **Web**: Scraping any website URL.
    - **Database**: Direct extraction from MySQL tables.
- **Smart Deduplication**: MD5 hashing ensures unique content and prevents index bloat.
- **Advanced Filtering**: Filter search results by department (HR, Finance, IT) for better precision.
- **Modular Services**: Clean separation of parsing, vector storage, and LLM logic.

## Project Structure
PROJECT3-4/
│── app/
│   ├── config.py       # Configuration & MySQL setup
│── services/
│   ├── parser.py       # Multi-source data extraction
│   ├── vector_store.py  # FAISS, Hashing, and Filtering
│   ├── llm.py           # Groq Llama 3 integration
│── ui/
│   ├── streamlit_app.py # Pro UI with Side-by-Side View
│── vectorstore/        # Local FAISS persistence

## How to Run

1. Configure your `.env` in the root:
   - `GROQ_API_KEY`
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (For MySQL ingestion)

2. Run the application:
```bash
poetry run streamlit run ui/streamlit_app.py
```
