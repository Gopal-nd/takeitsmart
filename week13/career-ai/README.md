# ResumeIQ AI

AI Career Coach that analyzes your resume and answers questions based on its content.

## Project Structure

CAREER-AI/
│── app/
│   ├── config.py       # Configuration and Env loading
│   ├── main.py         # FastAPI routes
│── services/
│   ├── parser.py       # PDF/DOCX/TXT parsing
│   ├── vector_store.py # FAISS logic
│   ├── coach.py        # LangChain logic
│── ui/
│   ├── streamlit_app.py # Streamlit interface
│── .env                # API Keys
│── .gitignore          # Git ignore
│── faiss_store/        # Local vector database

## Installation

This project is part of a Poetry workspace.
1. Configure `.env` with `GROQ_API_KEY`.
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
