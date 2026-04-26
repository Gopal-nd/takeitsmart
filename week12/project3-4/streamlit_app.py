import streamlit as st
from app.main import setup_pipeline

st.set_page_config(page_title="Enterprise RAG Chatbot")

st.title("💼 Enterprise Knowledge Chatbot")

if "chain" not in st.session_state:
    st.session_state.chain = setup_pipeline()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ CACHE (prevents repeated API calls)
if "cache" not in st.session_state:
    st.session_state.cache = {}

query = st.text_input("Ask your question:")

if query:
    if query in st.session_state.cache:
        answer = st.session_state.cache[query]
    else:
        response = st.session_state.chain(query)
        answer = response["answer"]
        st.session_state.cache[query] = answer

    st.session_state.chat_history.append(("You", query))
    st.session_state.chat_history.append(("Bot", answer))

for role, msg in st.session_state.chat_history:
    st.write(f"**{role}:** {msg}")