import streamlit as st
import numpy as np
import pickle

model = pickle.load(open("wine_model.pkl", "rb"))
scaler = pickle.load(open("wine_scaler.pkl", "rb"))
features = pickle.load(open("wine_features.pkl", "rb"))

st.title("🍷 Wine Classification App")

input_data = []

for feature in features:
    value = st.number_input(feature, value=0.0)
    input_data.append(value)

input_data = np.array(input_data).reshape(1, -1)
input_data = scaler.transform(input_data)

if st.button("Predict"):
    prediction = model.predict(input_data)
    st.success(f"Wine Class: {prediction[0]}")