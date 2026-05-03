from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
import shutil
import os
from app.config import DATA_PATH
from services.document_loader import load_pdf
from services.vector_store import create_vector_store
from services.rag_pipeline import get_answer

app = FastAPI(title="AI Medical Assistant - Bedrock")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(DATA_PATH, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        docs = load_pdf(file_path)
        create_vector_store(docs)

        return {"message": "File uploaded and indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask")
async def ask_question(query: str):
    try:
        answer, docs = get_answer(query)

        return {
            "answer": answer,
            "sources": [doc.metadata for doc in docs]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Medical AI Assistant running 🚀"}
