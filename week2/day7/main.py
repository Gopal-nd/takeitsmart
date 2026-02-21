import streamlit as st
import pandas as pd
import os

file_name = "inventory.xlsx"

# -----------------------------
# Initialize Excel File
# -----------------------------
def init_excel():
    if not os.path.exists(file_name):
        df = pd.DataFrame(columns=["Product", "Price", "Stock"])
        df.to_excel(file_name, index=False)

# -----------------------------
# Load Data
# -----------------------------
def load_inventory():
    return pd.read_excel(file_name)

# -----------------------------
# Save Data
# -----------------------------
def save_inventory(df):
    df.to_excel(file_name, index=False)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Inventory Manager", layout="centered")
st.title("📦 Inventory Management System")

init_excel()

menu = st.sidebar.radio(
    "Menu",
    ["Add Product", "Remove Product", "Search Product",
     "Update Stock", "View Inventory", "Total Inventory Value"]
)

df = load_inventory()

# --------------------------------------------------
# 1️⃣ Add Product
# --------------------------------------------------
if menu == "Add Product":
    st.subheader("Add New Product")

    product = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock Quantity", min_value=0)

    if st.button("Add Product"):
        if not product:
            st.warning("Please enter product name")
        elif product in df["Product"].values:
            st.error("Product already exists")
        else:
            new_row = pd.DataFrame({
                "Product": [product],
                "Price": [price],
                "Stock": [stock]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            save_inventory(df)
            st.success("Product added successfully!")

# --------------------------------------------------
# 2️⃣ Remove Product
# --------------------------------------------------
elif menu == "Remove Product":
    st.subheader("Remove Product")

    if not df.empty:
        product = st.selectbox("Select Product", df["Product"])

        if st.button("Remove"):
            df = df[df["Product"] != product]
            save_inventory(df)
            st.success("Product removed successfully!")
    else:
        st.info("No products available")

# --------------------------------------------------
# 3️⃣ Search Product
# --------------------------------------------------
elif menu == "Search Product":
    st.subheader("Search Product")

    search_term = st.text_input("Enter product name")

    if st.button("Search"):
        result = df[df["Product"].str.contains(search_term, case=False, na=False)]

        if not result.empty:
            st.dataframe(result)
        else:
            st.error("Product not found")

# --------------------------------------------------
# 4️⃣ Update Stock
# --------------------------------------------------
elif menu == "Update Stock":
    st.subheader("Update Stock")

    if not df.empty:
        product = st.selectbox("Select Product", df["Product"])
        new_stock = st.number_input("New Stock Quantity", min_value=0)

        if st.button("Update"):
            df.loc[df["Product"] == product, "Stock"] = new_stock
            save_inventory(df)
            st.success("Stock updated successfully!")
    else:
        st.info("No products available")

# --------------------------------------------------
# 5️⃣ View Inventory
# --------------------------------------------------
elif menu == "View Inventory":
    st.subheader("Current Inventory")

    if df.empty:
        st.info("Inventory is empty")
    else:
        st.dataframe(df)

# --------------------------------------------------
# 6️⃣ Total Inventory Value
# --------------------------------------------------
elif menu == "Total Inventory Value":
    st.subheader("Inventory Value")

    if df.empty:
        st.info("Inventory is empty")
    else:
        df["Total Value"] = df["Price"] * df["Stock"]
        total_value = df["Total Value"].sum()

        st.dataframe(df)
        st.success(f"Total Inventory Value: ₹ {total_value:,.2f}")