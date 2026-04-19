import os

import streamlit as st
from transformers import pipeline, CLIPProcessor, CLIPModel
from PIL import Image
import torch

st.set_page_config(page_title="Transformers Playground", page_icon="🤖", layout="wide")

st.title("🤖 AI Playground with Transformers")
st.write("Explore different machine learning capabilities including Sentiment Analysis, Text Generation, Image Classification, and Speech Recognition.")

@st.cache_resource
def get_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="AdamCodd/tinybert-sentiment-amazon")

@st.cache_resource
def get_generator_pipeline():
    return pipeline("text-generation", model="distilgpt2")

@st.cache_resource
def get_image_classifier_pipeline():
    return pipeline("image-classification", model="google/vit-base-patch16-224")

@st.cache_resource
def get_asr_pipeline():
    return pipeline("automatic-speech-recognition", model="openai/whisper-tiny")

@st.cache_resource
def load_clip():
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return model, processor


task = st.selectbox(
    "Choose a task to explore:",
    ["Sentiment Analysis", "Text Generation", "Image Classification", "Automatic Speech Recognition"]
)

st.divider()

# ---------------- SENTIMENT ----------------
if task == "Sentiment Analysis":
    st.subheader("📝 Sentiment Analysis")
    text = st.text_area("Enter text to analyze sentiment:", "I love using transformers for AI projects!")

    if st.button("Analyze Sentiment", type="primary"):
        with st.spinner("Downloading/Loading model (only takes a moment on first run)..."):
            sentiment_pipe = get_sentiment_pipeline()
        with st.spinner("Analyzing..."):
            result = sentiment_pipe(text)[0]
            st.success(f"**Sentiment**: {result['label']}")
            st.info(f"**Confidence Score**: {result['score']:.4f}")

# ---------------- TEXT GENERATION ----------------
elif task == "Text Generation":
    st.subheader("✍️ Text Generation")
    prompt = st.text_area("Enter a prompt to continue:", "Once upon a time in a futuristic city")

    if st.button("Generate Text", type="primary"):
        with st.spinner("Downloading/Loading model (only takes a moment on first run)..."):
            generator_pipe = get_generator_pipeline()
        with st.spinner("Generating text..."):
            result = generator_pipe(
                prompt,
                max_length=100,
                num_return_sequences=1
            )[0]
            st.write("### Generated Result:")
            st.write(result["generated_text"])

# ---------------- IMAGE CLASSIFICATION ----------------
elif task == "Image Classification":
    st.subheader("🖼️ Image Classification")
    uploaded_file = st.file_uploader("Upload an image to classify", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Display the uploaded image
        st.image(image, caption="Uploaded Image", width=400)

        if st.button("Classify Image", type="primary"):
            with st.spinner("Downloading/Loading model..."):
                image_pipe = get_image_classifier_pipeline()
            with st.spinner("Classifying..."):
                results = image_pipe(image)
                st.write("### Predictions:")
                for res in results[:3]:  # Show top 3 predictions
                    st.write(f"- **{res['label']}**: {res['score']:.4f}")

# ---------------- ASR ----------------
elif task == "Automatic Speech Recognition":
    st.subheader("🎙️ Automatic Speech Recognition")
    st.write("Upload an audio file to transcribe to text.")
    uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac"])

    if uploaded_file is not None:
        st.audio(uploaded_file)

        if st.button("Recognize Speech", type="primary"):
            with st.spinner("Downloading/Loading audio model (might take a minute)..."):
                asr_pipe = get_asr_pipeline()
            with st.spinner("Transcribing..."):
                result = asr_pipe(uploaded_file.read())
                st.write("### Transcription:")
                st.success(result["text"])
