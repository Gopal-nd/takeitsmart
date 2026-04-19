import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Emotion AI App", page_icon="🙂", layout="centered")

@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None
    )

st.title("🙂 Emotion-Aware AI App")
st.write("Detect emotions from text using an advanced Transformer model")

with st.spinner("Loading AI model..."):
    emotion_classifier = load_model()

def get_emotions(text):
    results = emotion_classifier(text)
    if isinstance(results[0], list):
        results = results[0]
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

user_text = st.text_area("Enter your text to analyze its emotional tone:")

if st.button("Analyze Emotion", type="primary"):
    if user_text.strip() != "":
        emotions = get_emotions(user_text)

        top = emotions[0]
        st.success(f"Top Emotion: **{top['label'].title()}** ({round(top['score']*100,2)}%)")

        st.subheader("Detailed Emotion Breakdown")
        
        for e in emotions:
            label = e['label'].title()
            score = float(e["score"])
            percent = round(score*100, 2)
            st.write(f"{label} ({percent}%)")
            st.progress(score)
    else:
        st.warning("Please enter some text to analyze!")
