import streamlit as st
import tempfile
from pathlib import Path

from embeddings import load_model
from ingestion import load_documents_from_file, upload_to_pinecone
from vector_store import init_pinecone
from retriever import retrieve
from llm import ask_llm

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("🤖 RAG Chatbot (Pinecone)")

top_k = st.sidebar.slider("Top K Results", 1, 10, 3)

# Session state flags
if "indexed" not in st.session_state:
    st.session_state.indexed = False

uploaded_file = st.file_uploader("Upload TXT file", type=["txt"])

if uploaded_file:

    temp_path = Path(tempfile.gettempdir()) / uploaded_file.name

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    model = load_model()
    index = init_pinecone()

    # 🚀 ONLY RUN ONCE
    if not st.session_state.indexed:
          docs = load_documents_from_file(temp_path)

    # 🔥 CLEAR OLD DATA (VERY IMPORTANT)
          index.delete(delete_all=True)

          upload_to_pinecone(docs, model, index)

          st.session_state.indexed = True
          st.success("Document indexed!")

    query = st.text_input("Ask something")

    if query:
        retrieved_docs = retrieve(query, model, index, top_k)

        context_texts = [doc["text"] for doc in retrieved_docs]

        answer = ask_llm(query, context_texts)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Retrieved Context")

        for d in retrieved_docs:
               st.markdown(f"""
        **Score:** {d['score']:.4f}  
        **Context:**  
        {d['text']}
        """)