import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS

# File parsing
from io import BytesIO
from docx import Document
import PyPDF2

# -----------------------------
# Ask for API key at server start
# -----------------------------
api_key = input("Enter your OpenAI API Key: ").strip()
if not api_key:
    print("OpenAI API key is required. Exiting...")
    exit()
os.environ["OPENAI_API_KEY"] = api_key

# -----------------------------
# App Initialization
# -----------------------------
app = FastAPI(title="AI Career Assistant API")

# Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FAISS folder
DB_PATH = "faiss_store"

# Embeddings
embeddings = OpenAIEmbeddings()

# -----------------------------
# Helper Functions
# -----------------------------
llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)  # uses api_key automatically

def load_vectorstore():
    if os.path.exists(DB_PATH) and os.path.isdir(DB_PATH):
        return FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    return None

def save_vectorstore(vectorstore):
    vectorstore.save_local(DB_PATH)

def store_resume(user_id: str, text: str):
    vectorstore = load_vectorstore()
    if vectorstore is None:
        vectorstore = FAISS.from_texts(
            [text],
            embeddings,
            metadatas=[{"user_id": user_id}]
        )
    else:
        vectorstore.add_texts(
            [text],
            metadatas=[{"user_id": user_id}]
        )
    save_vectorstore(vectorstore)

def retrieve_context(user_id: str, query: str, k: int = 3):
    vectorstore = load_vectorstore()
    if vectorstore is None:
        return ""
    results = vectorstore.similarity_search(query, k=k)
    filtered = [
        r.page_content for r in results if r.metadata.get("user_id") == user_id
    ]
    return "\n".join(filtered)

def generate_answer(user_id: str, question: str):
    context = retrieve_context(user_id, question)
    if not context:
        return "⚠️ No resume found. Please upload a resume first."

    prompt = ChatPromptTemplate.from_template(
        """
You are an expert AI Career Coach.

Use the resume context below to answer the question.

Resume:
{context}

Question:
{question}

Answer clearly and professionally.
"""
    )
    chain = prompt | llm
    response = chain.invoke({"context": context, "question": question})
    return response.content

# -----------------------------
# File Parsing Helper
# -----------------------------
def extract_text(file: UploadFile) -> str:
    filename = file.filename.lower()
    content = file.file.read()
    
    if filename.endswith(".txt"):
        return content.decode("utf-8")
    
    elif filename.endswith(".docx"):
        doc = Document(BytesIO(content))
        return "\n".join([p.text for p in doc.paragraphs])
    
    elif filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only .txt, .docx, .pdf allowed.")

# -----------------------------
# API Models
# -----------------------------
class QuestionRequest(BaseModel):
    user_id: str
    question: str

class QuestionResponse(BaseModel):
    answer: str

# -----------------------------
# Routes
# -----------------------------
@app.post("/upload_resume")
async def upload_resume(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        text = extract_text(file)
        store_resume(user_id, text)
        return {"status": "success", "message": "Resume uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        answer = generate_answer(request.user_id, request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "AI Career Assistant API is running!"}