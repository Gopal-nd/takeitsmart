import streamlit as st
from coordinator import Coordinator

st.set_page_config(page_title="Multi-Agent AI", layout="wide")

st.title("🤖 Multi-Agent AI System")
st.write("Upload a document and let AI agents analyze it from different perspectives.")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.subheader("📄 Original Document")
    st.text_area("Document Text", text, height=300)

    if st.button("Analyze with Agents"):
        with st.spinner("Agents are analyzing..."):
            coordinator = Coordinator()
            results = coordinator.run_all(text)

        st.subheader("🔍 Agent Results")

        for agent_name, result in results.items():
            st.markdown(f"### {agent_name}")
            st.write(result)