import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="ResumeIQ AI", layout="wide")

st.title("💼 ResumeIQ AI")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

# Sidebar
st.sidebar.header("User Setup")

user_id = st.sidebar.text_input("User ID")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"]
)

if st.sidebar.button("Upload Resume"):
    if not user_id:
        st.sidebar.error("Enter user ID")
    elif not uploaded_file:
        st.sidebar.error("Upload a file")
    else:
        with st.sidebar:
            with st.spinner("Uploading..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"user_id": user_id}

                res = requests.post(
                    f"{API_URL}/upload",
                    files=files,
                    data=data
                )

                if res.status_code == 200:
                    st.success("Resume uploaded ✅")
                    st.session_state.resume_uploaded = True
                else:
                    st.error(res.text)

# Chat UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if st.session_state.resume_uploaded:
    prompt = st.chat_input("Ask about your resume...")
else:
    st.info("Please upload a resume in the sidebar to start chatting.")
    prompt = None

if prompt:
    if not user_id:
        st.warning("Please enter user ID first")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            res = requests.post(
                f"{API_URL}/ask",
                json={
                    "user_id": user_id,
                    "question": prompt
                }
            )

            if res.status_code == 200:
                answer = res.json()["answer"]
                st.write(answer)
            else:
                answer = "Error occurred"
                st.error(res.text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
