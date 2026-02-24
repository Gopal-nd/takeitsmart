import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.title("Sales Dashboard")

data = pd.read_csv("sales.csv")
print("Loaded Successfully!")

region = st.selectbox("Select Region", data["Region"].unique())
filtered = data[data["Region"] == region]

fig, ax = plt.subplots()
sns.barplot(x="Category", y="Sales", data=filtered, ax=ax)
st.pyplot(fig)