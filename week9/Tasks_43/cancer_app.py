import streamlit as st
import numpy as np
import pickle

# Load saved files
model = pickle.load(open("cancer_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
features = pickle.load(open("features.pkl", "rb"))

# Title
st.title("🧬 Breast Cancer Prediction App")
st.write("Enter the key medical values to predict tumor type.")

# Input fields
input_data = []

for feature in features:
    value = st.number_input(f"{feature}", value=0.0)
    input_data.append(value)

# Convert to array
input_data = np.array(input_data).reshape(1, -1)

# Apply scaling
input_data = scaler.transform(input_data)

# Prediction
if st.button("Predict"):
    prediction = model.predict(input_data)

    if prediction[0] == 0:
        st.error("⚠️ Malignant (Cancerous)")
    else:
        st.success("✅ Benign (Non-Cancerous)")