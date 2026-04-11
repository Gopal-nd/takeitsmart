import streamlit as st
import pandas as pd
import pickle
import requests

# ==============================
# 📚 Helper function for poster
# ==============================
def fetch_poster(thumbnail):
    if pd.isna(thumbnail) or not isinstance(thumbnail, str) or thumbnail.strip() == "":
        return "https://via.placeholder.com/150x200?text=No+Cover"
    return thumbnail

# ==============================
# 📂 Load data with cache
# ==============================
@st.cache_data
def load_data():
    books_dict = pickle.load(open('book_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return pd.DataFrame(books_dict), similarity

books, similarity = load_data()

# ==============================
# 🤖 Recommendation function
# ==============================
def recommend(book):
    if book not in books['title'].values:
        return [], []

    book_index = books[books['title'] == book].index[0]
    distances = similarity[book_index]

    books_list = sorted(
        enumerate(distances),
        key=lambda x: x[1],
        reverse=True
    )

    recommended_books = []
    recommended_posters = []

    for i in books_list[1:6]:
        recommended_books.append(books.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(books.iloc[i[0]]['thumbnail']))

    return recommended_books, recommended_posters

# ==============================
# 🎨 Streamlit UI
# ==============================
st.title("📚 Books Recommender System")

selected_book = st.selectbox(
    "Choose a book",
    books['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_book)

    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.markdown(f"**{names[i]}**")
                st.image(posters[i], use_container_width=True)
    else:
        st.warning("Book not found!")