from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.config import validate_config
from services.parser import extract_text
from services.vector_store import store_resume
from services.coach import generate_answer

# Initialize config
validate_config()

app = FastAPI(title="ResumeIQ AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    user_id: str
    question: str

@app.post("/upload")
async def upload_resume(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        text = extract_text(file)

        if not text.strip():
            raise HTTPException(400, "Empty or unreadable file")

        store_resume(user_id, text)

        return {
            "status": "success",
            "message": "Resume uploaded successfully"
        }

    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/ask")
async def ask_question(request: Question):
    try:
        answer = generate_answer(
            request.user_id,
            request.question
        )

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/")
def root():
    return {"message": "ResumeIQ AI running 🚀"}
