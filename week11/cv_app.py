import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Streamlit app config
st.set_page_config(page_title="Face Detection App", page_icon="👁️", layout="centered")
st.title("👁️ Face Detection using OpenCV")
st.markdown("### Upload an image and detect faces instantly!")

# Load the Haar cascade model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read and convert image
    img = np.array(Image.open(uploaded_file))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(img, "Face", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 0, 0), 2, cv2.LINE_AA)
    
    st.image(img, caption=f"Detected {len(faces)} face(s)", use_container_width=True)
else:
    st.info("📸 Upload a clear photo to start detecting faces.")
