import streamlit as st
import sys
import os

# Ensure the root of the project is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
from services.bedrock import BedrockChatbot

# Page config
st.set_page_config(page_title="LLaMA 3 Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 LLaMA 3 Chatbot")
st.caption("Powered by AWS Bedrock (Cost Optimized)")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = None

if "message_count" not in st.session_state:
    st.session_state.message_count = 0


# Sidebar
with st.sidebar:
    st.header("⚙ AWS Configuration")

    aws_access_key = st.text_input(
        "AWS Access Key ID",
        value=AWS_ACCESS_KEY_ID,
        type="password"
    )

    aws_secret_key = st.text_input(
        "AWS Secret Access Key",
        value=AWS_SECRET_ACCESS_KEY,
        type="password"
    )

    region = st.selectbox("AWS Region", ["ap-south-1", "us-east-1", "us-west-2"])

    connect = st.button("🚀 Connect")


# Connect
if connect:
    try:
        st.session_state.chatbot = BedrockChatbot(
            aws_access_key=aws_access_key,
            aws_secret_key=aws_secret_key,
            region=region
        )
        st.sidebar.success("✅ Connected")
    except Exception as e:
        st.sidebar.error(f"❌ {e}")


# Chat UI
if st.session_state.chatbot:

    # 🚨 HARD LIMIT (₹10 protection)
    if st.session_state.message_count >= 25:
        st.warning("🚫 Demo limit reached (cost protection enabled)")
        st.stop()

    col1, col2 = st.columns([8, 1])

    with col1:
        user_input = st.text_input("Message", placeholder="Type...", label_visibility="collapsed")

    with col2:
        send = st.button("Send")

    if send and user_input.strip():

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            output_text = st.session_state.chatbot.invoke(user_input)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": output_text
            })

            # count messages
            st.session_state.message_count += 1

        except Exception as e:
            st.error(f"❌ {e}")

    st.markdown("---")

    for turn in st.session_state.chat_history:
        if turn["role"] == "user":
            st.markdown(f"🧑 **You:** {turn['content']}")
        else:
            st.markdown(f"🤖 **Bot:** {turn['content']}")

else:
    st.info("Enter AWS credentials and connect 🚀")
