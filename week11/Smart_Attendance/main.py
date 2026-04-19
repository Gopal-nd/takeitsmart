import streamlit as st
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Smart Attendance", page_icon="📸", layout="centered")

st.title("📸 Smart Attendance System")
st.write("Detect faces and log your attendance.")

# File to store attendance logs within the same directory
ATTENDANCE_FILE = "attendance_log.csv"

# Initialize CSV if it doesn't exist
if not os.path.exists(ATTENDANCE_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    df.to_csv(ATTENDANCE_FILE, index=False)

# Load the Haar cascade model
@st.cache_resource
def load_cascade():
    return cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

face_cascade = load_cascade()

name_input = st.text_input("Enter your Name:")
img_file = st.camera_input("Take a picture to mark attendance")

if img_file is not None:
    if name_input.strip() == "":
        st.warning("Please enter your name before taking a picture.")
    else:
        # Process image
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            st.image(img, caption=f"Detected {len(faces)} face(s). Attendance Marked!", channels="BGR")
            
            # Log attendance
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            
            df = pd.read_csv(ATTENDANCE_FILE)
            
            # Check if already marked today
            if not ((df['Name'] == name_input) & (df['Date'] == date_str)).any():
                new_row = pd.DataFrame([{"Name": name_input, "Date": date_str, "Time": time_str, "Status": "Present"}])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(ATTENDANCE_FILE, index=False)
                st.success(f"Attendance successfully logged for {name_input}!")
            else:
                st.info(f"{name_input} is already marked present for today.")
        else:
            st.error("No face detected. Please ensure your face is clearly visible and try again.")

st.divider()
st.subheader("📋 Today's Attendance Log")
if os.path.exists(ATTENDANCE_FILE):
    df = pd.read_csv(ATTENDANCE_FILE)
    today_str = datetime.now().strftime("%Y-%m-%d")
    today_df = df[df['Date'] == today_str]
    st.dataframe(today_df, use_container_width=True)
