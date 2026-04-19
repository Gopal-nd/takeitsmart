import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )

emotion_classifier = load_model()

def get_emotions(text):
    results = emotion_classifier(text)
    if isinstance(results[0], list):
        results = results[0]
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

st.set_page_config(page_title="Emotion AI App", layout="centered")

st.title("😊 Emotion-Aware AI App")
st.write("Detect emotions from text using Transformer models")

user_text = st.text_area("Enter your text:")

if st.button("Analyze Emotion"):
    if user_text.strip() != "":
        emotions = get_emotions(user_text)

        top = emotions[0]
        st.success(f"Top Emotion: {top['label']} ({round(top['score']*100,2)}%)")

        st.subheader("Detailed Emotion Breakdown")

        for e in emotions:
            st.write(f"{e['label']} ({round(e['score']*100,2)}%)")
            st.progress(float(e["score"]))
    else:
        st.warning("Please enter some text!")
