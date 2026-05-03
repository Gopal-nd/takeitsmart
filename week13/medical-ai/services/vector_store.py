from langchain_community.vectorstores import FAISS
from services.embeddings import get_embeddings
from app.config import DB_PATH

def create_vector_store(docs):
    embedding = get_embeddings()
    db = FAISS.from_documents(docs, embedding)
    db.save_local(DB_PATH)

def load_vector_store():
    embedding = get_embeddings()
    return FAISS.load_local(DB_PATH, embedding, allow_dangerous_deserialization=True)
