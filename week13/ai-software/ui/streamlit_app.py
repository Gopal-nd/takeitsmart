# ui/streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="AI Software Team", layout="wide")

st.title("🤖 AI Software Development Team")

idea = st.text_input("Enter your project idea")

if st.button("Build Project"):
    with st.spinner("Agents working..."):
        res = requests.post(
            "http://localhost:8000/build",
            json={"idea": idea}
        )

        data = res.json()

        st.subheader("📌 Requirements")
        st.write(data["requirements"])

        st.subheader("🏗 Architecture")
        st.write(data["architecture"])

        st.subheader("⚙ Backend Code")
        st.code(data["backend_code"], language="python")

        st.subheader("🎨 Frontend Code")
        st.code(data["frontend_code"], language="javascript")

        st.subheader("🔍 Review")
        st.write(data["review"])

        st.subheader("🧪 Tests")
        st.write(data["tests"])

        st.subheader("🚀 Deployment")
        st.write(data["deployment"])