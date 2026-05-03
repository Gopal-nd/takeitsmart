import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Medical Assistant", layout="wide")

st.title("🩺 AI Medical Assistant (Llama 3)")

# Upload section
with st.sidebar:
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose file", type=["pdf"])

    if uploaded_file and st.button("Upload"):
        with st.spinner("Indexing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            res = requests.post(f"{API_URL}/upload", files=files)
            if res.status_code == 200:
                st.success("Indexed successfully!")
            else:
                st.error(f"Error: {res.text}")

# Chat
st.subheader("Ask Questions")

if "chat" not in st.session_state:
    st.session_state.chat = []

query = st.text_input("Enter your question")

if st.button("Ask") and query:
    with st.spinner("Consulting AI..."):
        res = requests.post(f"{API_URL}/ask", params={"query": query})
        if res.status_code == 200:
            answer = res.json()["answer"]
            st.session_state.chat.append((query, answer))
        else:
            st.error(f"Error: {res.text}")

for q, a in st.session_state.chat[::-1]:
    with st.chat_message("user"):
        st.write(q)
    with st.chat_message("assistant"):
        st.write(a)
