import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading data...")
movies = pd.read_csv('tmdb_5000_movies.xls')
credits = pd.read_csv('tmdb_5000_credits.xls')

print("Merging and filtering...")
movies = movies.merge(credits, on='title')
movies = movies[['id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
movies.dropna(inplace=True)

def convert(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            L.append(i['name'])
    except:
        pass
    return L

def convert_cast(text):
    L = []
    counter = 0
    try:
        for i in ast.literal_eval(text):
            if counter < 3:
                L.append(i['name'])
            counter += 1
    except:
        pass
    return L

def fetch_director(text):
    L = []
    try:
        for i in ast.literal_eval(text):
            if i['job'] == 'Director':
                L.append(i['name'])
                break
    except:
        pass
    return L

print("Processing columns...")
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(fetch_director)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['id', 'title', 'tags']].copy()
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
new_df.rename(columns={'id': 'movie_id'}, inplace=True)

print("Vectorizing...")
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

print("Calculating similarity...")
similarity = cosine_similarity(vectors)

print("Saving models...")
pickle.dump(new_df.to_dict(), open('movie_dict.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Done!")
