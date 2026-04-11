import streamlit as st
import numpy as np
import pickle

model = pickle.load(open("titanic_model.pkl", "rb"))
scaler = pickle.load(open("titanic_scaler.pkl", "rb"))

st.title("🚢 Titanic Survival Prediction")

pclass = st.selectbox("Passenger Class", [1,2,3])
sex = st.selectbox("Sex", ["Male", "male"])
age = st.number_input("Age", value=25)
sibsp = st.number_input("Siblings/Spouses", value=0)
parch = st.number_input("Parents/Children", value=0)
fare = st.number_input("Fare", value=50.0)
embarked = st.selectbox("Embarked", ["C","Q","S"])

# Encoding
sex = 1 if sex == "Male" else 0
embarked_map = {"C":0, "Q":1, "S":2}
embarked = embarked_map[embarked]

input_data = np.array([[pclass, sex, age, sibsp, parch, fare, embarked]])
input_data = scaler.transform(input_data)

if st.button("Predict"):
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("✅ Survived")
    else:
        st.error("❌ Not Survived")