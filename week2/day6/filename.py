import streamlit as st
import pandas as pd

st.title("🎓 Streamlit Assignment App")

# ---------------------------------------------------
# 1️⃣ Display Name, Role, Skills
# ---------------------------------------------------

st.header("My Profile")

st.write("Name: Gopal N D")
st.write("Role: MERN Stack Developer")
st.write("Skills: React, Next.js, Prisma, PostgreSQL, Machine Learning")

# ---------------------------------------------------
# 2️⃣ Take User Input (Name & Age)
# ---------------------------------------------------

st.header("User Input Section")

name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0, max_value=100)

if st.button("Submit"):
    st.success(f"Hello {name}, you are {age} years old!")

# ---------------------------------------------------
# 3️⃣ Checkbox Show/Hide Text
# ---------------------------------------------------

st.header("Checkbox Example")

if st.checkbox("Show Message"):
    st.write("This text is visible because checkbox is selected")

# ---------------------------------------------------
# 4️⃣ Selectbox Example
# ---------------------------------------------------

language = st.selectbox("Choose Programming Language",
                         ["Python", "Java", "C++", "JavaScript"])

st.write("You selected:", language)

# ---------------------------------------------------
# 5️⃣ Simple Counter using Button
# ---------------------------------------------------

st.header("Counter Example")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increase Counter"):
    st.session_state.count += 1

st.write("Counter Value:", st.session_state.count)

# ---------------------------------------------------
# 6️⃣ Display DataFrame
# ---------------------------------------------------

st.header("Display DataFrame")

data = {
    "Name": ["A", "B", "C"],
    "Salary": [40000, 60000, 75000]
}

df = pd.DataFrame(data)

st.dataframe(df)

# ---------------------------------------------------
# 7️⃣ Upload CSV and Display
# ---------------------------------------------------

st.header("Upload CSV File")

file = st.file_uploader("Upload CSV File", type=["csv"])

if file is not None:
    df_uploaded = pd.read_csv(file)
    st.write("Uploaded Data:")
    st.dataframe(df_uploaded)

# ---------------------------------------------------
# 8️⃣ Display Image
# ---------------------------------------------------

st.header("Display Image")

st.image("https://via.placeholder.com/300", caption="Sample Image")

# ---------------------------------------------------
# 9️⃣ Sidebar Menu
# ---------------------------------------------------

st.sidebar.title("Courses Menu")

course = st.sidebar.selectbox(
    "Choose Course",
    ["Data Science", "Full Stack Java", "Full Stack Python", "Dot Net"]
)

st.sidebar.write("You selected:", course)

# ---------------------------------------------------
# 🔟 Success Message Button
# ---------------------------------------------------

if st.button("Click for Success"):
    st.success("Button Clicked Successfully!")

# ---------------------------------------------------
# 🔹 TASK 1: Filter Employees Salary > 50000
# ---------------------------------------------------

st.header("Filter Employees Salary > 50000")

if st.checkbox("Show High Salary Employees"):
    high_salary = df[df["Salary"] > 50000]
    st.dataframe(high_salary)

# ---------------------------------------------------
# 🔹 TASK 2: Display Content Based on Role Selection
# ---------------------------------------------------

st.header("Role Based Content")

role = st.selectbox("Select Your Role",
                    ["Student", "Developer", "Data Scientist"])

if role == "Student":
    st.write("You can learn Python and SQL.")
elif role == "Developer":
    st.write("You should learn React and Backend.")
elif role == "Data Scientist":
    st.write("You should focus on ML, Deep Learning and NLP.")