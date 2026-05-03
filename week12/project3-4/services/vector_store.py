from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib
import os
from app.config import DB_PATH

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def load_vectorstore():
    if os.path.exists(os.path.join(DB_PATH, "index.faiss")):
        return FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    return None

def save_vectorstore(vs):
    vs.save_local(DB_PATH)

def process_and_add(raw_docs):
    vs = load_vectorstore()
    chunks = splitter.split_documents(raw_docs)
    
    # Deduplication using MD5
    existing_hashes = set()
    if vs:
        # This is a simple way to get hashes if they exist in metadata
        # In a real enterprise app, we'd query more efficiently
        all_docs = vs.similarity_search("", k=10000)
        existing_hashes = {d.metadata.get("hash") for d in all_docs if "hash" in d.metadata}

    new_chunks = []
    for chunk in chunks:
        chunk_hash = hashlib.md5(chunk.page_content.encode()).hexdigest()
        if chunk_hash not in existing_hashes:
            chunk.metadata["hash"] = chunk_hash
            new_chunks.append(chunk)

    if new_chunks:
        if vs is None:
            vs = FAISS.from_documents(new_chunks, embeddings)
        else:
            vs.add_documents(new_chunks)
        save_vectorstore(vs)
    
    return len(new_chunks)

def retrieve_docs(query, department="All"):
    vs = load_vectorstore()
    if not vs:
        return []
    
    # Search
    docs = vs.similarity_search(query, k=5)
    
    # Filter by department
    if department != "All":
        docs = [d for d in docs if d.metadata.get("department") == department]
        
    return docs
