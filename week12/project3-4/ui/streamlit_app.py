import streamlit as st
import os
import sys
from langchain_core.documents import Document

# Path fix for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.parser import read_pdf, read_docx, read_csv, read_txt, read_website, read_mysql_database, detect_department
from services.vector_store import process_and_add, retrieve_docs
from services.llm import ask_llm

st.set_page_config(page_title="Enterprise Multi-Doc RAG", page_icon="📚", layout="wide")

st.title("📚 Enterprise Multi-Doc RAG System")
st.markdown("Knowledge retrieval across Files, Web, and Databases.")

# Sidebar for Ingestion
with st.sidebar:
    st.header("📥 Data Ingestion")
    
    uploaded_files = st.file_uploader(
        "Upload files (PDF, DOCX, CSV, TXT)",
        type=["pdf", "docx", "csv", "txt"],
        accept_multiple_files=True
    )
    
    web_url = st.text_input("🌐 Website URL")
    
    db_table = st.selectbox(
        "🗄️ Database Table",
        ["None", "employees", "policies", "attendance"]
    )
    
    if st.button("🚀 Process & Index"):
        docs = []
        
        # Process Files
        if uploaded_files:
            for file in uploaded_files:
                text = ""
                if file.name.endswith(".pdf"): text = read_pdf(file)
                elif file.name.endswith(".docx"): text = read_docx(file)
                elif file.name.endswith(".csv"): text = read_csv(file)
                elif file.name.endswith(".txt"): text = read_txt(file)
                
                if text.strip():
                    docs.append(Document(
                        page_content=text,
                        metadata={"source": file.name, "department": detect_department(file.name), "type": "file"}
                    ))
        
        # Process Web
        if web_url:
            text = read_website(web_url)
            if text.strip():
                docs.append(Document(page_content=text, metadata={"source": web_url, "type": "web"}))
        
        # Process DB
        if db_table != "None":
            text = read_mysql_database(db_table)
            if text.strip():
                docs.append(Document(page_content=text, metadata={"source": f"db:{db_table}", "type": "database"}))

        if docs:
            new_count = process_and_add(docs)
            st.success(f"✅ Indexed {new_count} new unique chunks!")
        else:
            st.warning("No new content to index.")

# Main Chat Section
st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Query Knowledge Base")
    dept_filter = st.selectbox("🎯 Filter by Department", ["All", "HR", "Finance", "IT", "General"])
    query = st.chat_input("Ask a question...")

    if query:
        with st.spinner("Analyzing..."):
            retrieved = retrieve_docs(query, department=dept_filter)
            context = "\n\n".join([d.page_content for d in retrieved])
            
            answer = ask_llm(context, query)
            
            with st.chat_message("user"):
                st.write(query)
            with st.chat_message("assistant"):
                st.write(answer)

with col2:
    st.subheader("🔍 Sources")
    if query and retrieved:
        for d in retrieved:
            with st.expander(f"📄 {d.metadata.get('source')}"):
                st.write(d.page_content[:300] + "...")
                st.caption(f"Type: {d.metadata.get('type')} | Dept: {d.metadata.get('department', 'N/A')}")
    else:
        st.info("Retrieve information to see sources here.")
