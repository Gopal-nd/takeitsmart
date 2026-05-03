import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import DB_PATH

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_vectorstore():
    if os.path.exists(DB_PATH):
        return FAISS.load_local(
            DB_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
    return None

def save_vectorstore(vs):
    vs.save_local(DB_PATH)

def store_resume(user_id: str, text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)
    metadatas = [{"user_id": user_id} for _ in chunks]

    vs = load_vectorstore()

    if vs is None:
        vs = FAISS.from_texts(chunks, embeddings, metadatas=metadatas)
    else:
        vs.add_texts(chunks, metadatas=metadatas)

    save_vectorstore(vs)

def retrieve_context(user_id: str, query: str, k: int = 4):
    vs = load_vectorstore()
    if not vs:
        return ""

    # Use filter to only get results for this user
    docs = vs.similarity_search(query, k=k, filter={"user_id": user_id})

    return "\n".join([d.page_content for d in docs])
