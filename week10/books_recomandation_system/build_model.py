import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

def main():
    print("Loading data...")
    # Read the dataset
    df = pd.read_csv('books (2).xls')
    
    print("Processing data...")
    # Select relevant features
    df = df[['isbn13', 'title', 'authors', 'categories', 'description', 'thumbnail']]
    
    # Drop rows without title
    df = df.dropna(subset=['title']).copy()
    
    # Fill NaN values with empty strings for text features
    for col in ['authors', 'categories', 'description']:
        df[col] = df[col].fillna('')
    
    # Create tags by combining features
    df['tags'] = df['authors'] + " " + df['categories'] + " " + df['description']
    df['tags'] = df['tags'].apply(lambda x: str(x).lower())
    
    # Remove duplicates based on title and reset index
    df = df.drop_duplicates(subset=['title']).reset_index(drop=True)
    
    print(f"Total unique books: {len(df)}")
    
    print("Vectorizing text...")
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    
    print("Calculating cosine similarity...")
    similarity = cosine_similarity(vectors)
    
    print("Saving models...")
    # Save the dataframe and similarity matrix
    pickle.dump(df.to_dict(), open('book_dict.pkl', 'wb'))
    pickle.dump(similarity, open('similarity.pkl', 'wb'))
    print("Done! Files saved as 'book_dict.pkl' and 'similarity.pkl'.")

if __name__ == "__main__":
    main()
