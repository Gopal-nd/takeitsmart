import streamlit as st
import tempfile
from pathlib import Path

from embeddings import load_model
from ingestion import load_documents_from_file
from vector_store import create_faiss_index
from retriever import retrieve
from llm import ask_llm

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("🤖 RAG Chatbot (FAISS)")

st.sidebar.title("⚙️ Settings")
top_k = st.sidebar.slider("Top K Results", 1, 10, 3)

uploaded_file = st.file_uploader("📄 Upload TXT file", type=["txt"])


# ✅ SESSION STATE INIT
if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.documents = None
    st.session_state.model = None


# ✅ RESET BUTTON
if st.sidebar.button("🔄 Upload New File"):
    st.session_state.index = None
    st.session_state.documents = None
    st.session_state.model = None


# ✅ CACHE LLM RESPONSE
@st.cache_data(show_spinner=False)
def cached_llm(query, context_tuple):
    return ask_llm(query, [{"document": doc} for doc in context_tuple])


if uploaded_file:

    if st.session_state.index is None:

        temp_dir = tempfile.gettempdir()
        filepath = Path(temp_dir) / uploaded_file.name

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Loading embedding model..."):
            st.session_state.model = load_model()

        documents = load_documents_from_file(filepath)
        st.session_state.documents = documents

        st.success(f"Loaded {len(documents)} chunks")

        with st.spinner("Creating FAISS index..."):
            st.session_state.index = create_faiss_index(
                documents,
                st.session_state.model
            )

    query = st.text_input("💬 Ask your question")

    if query and st.session_state.index is not None:

        with st.spinner("Retrieving relevant documents..."):
            results = retrieve(
                query,
                st.session_state.model,
                st.session_state.index,
                st.session_state.documents,
                top_k
            )

        context_tuple = tuple([r["document"] for r in results])

        with st.spinner("Generating answer..."):
            answer = cached_llm(query, context_tuple)

        # ✅ AI Answer (cleaner look)
        st.markdown("## 🤖 AI Answer")
        st.info(answer)

        # ✅ Retrieved Context (FIXED UI)
        st.markdown("## 🔎 Retrieved Context")

        for i, r in enumerate(results):
            if i == 0:
                title = "🟢 Best Match"
            else:
                title = f"🔹 Result {i+1}"

            st.markdown(f"### {title}")

            with st.container():
                st.markdown(f"""
                <div style="
                    background-color:#f1f5f9;
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:10px;
                    border:1px solid #cbd5e1;
                    color:#000000;
                ">
                    <b>Score:</b> {r['score']:.4f}<br><br>
                    {r['document']}
                </div>
                """, unsafe_allow_html=True)

else:
    st.info("📌 Upload a file to start")