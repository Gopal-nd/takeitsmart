import streamlit as st
import pandas as pd


# PAGE CONFIG

st.set_page_config(page_title="Ecommerce Analysis", layout="wide")


# LOAD DATA

df = pd.read_csv("final_data.csv")
rules = pd.read_csv("rules.csv")


# CLEAN FUNCTION

def clean_items(x):
    try:
        items = list(eval(x))
        return ", ".join(items)
    except:
        return x

rules['antecedents'] = rules['antecedents'].astype(str)
rules['consequents'] = rules['consequents'].astype(str)

rules['antecedents_clean'] = rules['antecedents'].apply(clean_items)
rules['consequents_clean'] = rules['consequents'].apply(clean_items)

# TITLE

st.markdown("<h1 style='text-align:center;'>🛒 Ecommerce Customer Analysis</h1>", unsafe_allow_html=True)
st.write("---")


# CUSTOMER SEGMENTATION

st.subheader("👤 Customer Segmentation")

col1, col2 = st.columns(2)

with col1:
    customer_id = st.selectbox("Select Customer ID", df['CustomerID'].unique())

with col2:
    if 'Cluster' in df.columns:
        cluster = df[df['CustomerID'] == customer_id]['Cluster'].values[0]
        st.metric(label="Customer Cluster", value=cluster)
    else:
        st.warning("Cluster data not available")

st.write("---")


# RECOMMENDATION SYSTEM

st.subheader("🛍️ Product Recommendations")

product = st.selectbox("Select Product", df['Product'].unique())


# FILTER RULES 

filtered = rules[
    rules['antecedents_clean'].str.contains(product, case=False, na=False)
]

# Remove duplicate recommendations
filtered = filtered.drop_duplicates(subset=['consequents_clean'])

# Sort by lift (best first)
filtered = filtered.sort_values(by='lift', ascending=False)

# Take top 3
top_rules = filtered.head(3)


# DISPLAY RESULTS

if not top_rules.empty:
    st.success(f"Top Recommendations for {product}")

    for _, row in top_rules.iterrows():
        st.markdown(f"""
        <div style="
            background-color:#1f2937;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
        ">
        👉 <b>If customer buys {product}</b><br>
        ➜ Recommend: <span style="color:#22c55e;"><b>{row['consequents_clean']}</b></span><br>
        📈 Lift: {round(row['lift'],2)}
        </div>
        """, unsafe_allow_html=True)

else:
    st.warning("No recommendations found")

st.write("---")


# OPTIONAL DATA VIEW

with st.expander("📊 View Sample Data"):
    st.dataframe(df.head())