import streamlit as st
import tempfile
import os
import sys
from pathlib import Path

# Add the project root to sys.path to allow importing from services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.embeddings import load_embedding_model
from services.ingestion import load_documents_from_file
from services.vector_store import FAISSStore, PineconeStore
from services.llm import ask_llm

st.set_page_config(page_title="Unified RAG Chatbot", layout="wide")

st.title("🤖 Unified RAG Chatbot")
st.caption("Switch between FAISS (Local) and Pinecone (Cloud)")

# Sidebar Settings
st.sidebar.title("⚙️ Settings")
vector_store_type = st.sidebar.radio("Select Vector Store", ["FAISS (Local)", "Pinecone (Cloud)"])
top_k = st.sidebar.slider("Top K Results", 1, 10, 3)

# Session State
if "store" not in st.session_state:
    st.session_state.store = None
if "indexed_file" not in st.session_state:
    st.session_state.indexed_file = None

# Model Loading
model = load_embedding_model()

# File Upload
uploaded_file = st.file_uploader("📄 Upload TXT file", type=["txt"])

if uploaded_file:
    # Check if we need to re-index
    if st.session_state.indexed_file != uploaded_file.name:
        
        with st.spinner(f"Indexing in {vector_store_type}..."):
            # Save temp file
            temp_path = Path(tempfile.gettempdir()) / uploaded_file.name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Load docs
            documents = load_documents_from_file(temp_path)
            
            # Initialize Store
            if vector_store_type == "FAISS (Local)":
                store = FAISSStore(model)
                store.create_index(documents)
            else:
                try:
                    store = PineconeStore(model)
                    store.upload_documents(documents)
                except Exception as e:
                    st.error(f"Pinecone Error: {e}")
                    st.stop()
            
            st.session_state.store = store
            st.session_state.indexed_file = uploaded_file.name
            st.success(f"Successfully indexed {len(documents)} chunks!")

    # Chat UI
    query = st.text_input("💬 Ask a question about the document")

    if query and st.session_state.store:
        with st.spinner("Retrieving and generating..."):
            results = st.session_state.store.search(query, k=top_k)
            context_texts = [r["text"] for r in results]
            
            answer = ask_llm(query, context_texts)
            
            st.markdown("### 🤖 AI Answer")
            st.info(answer)
            
            with st.expander("🔎 View Source Context"):
                for r in results:
                    st.markdown(f"**Score:** `{r['score']:.4f}`")
                    st.text(r["text"])
                    st.divider()
else:
    st.info("📌 Please upload a .txt file to start.")
    st.session_state.store = None
    st.session_state.indexed_file = None
