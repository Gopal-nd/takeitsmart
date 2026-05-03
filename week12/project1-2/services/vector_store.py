import faiss
import numpy as np
import os
from pinecone import Pinecone, ServerlessSpec
from app.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, FAISS_DB_PATH

class FAISSStore:
    def __init__(self, model):
        self.model = model
        self.index = None
        self.documents = []

    def create_index(self, documents):
        self.documents = documents
        embeddings = self.model.encode(documents)
        embeddings = np.array(embeddings).astype("float32")
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query, k=3):
        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for idx, doc_index in enumerate(indices[0]):
            results.append({
                "text": self.documents[doc_index],
                "score": float(distances[0][idx])
            })
        return results

class PineconeStore:
    def __init__(self, model):
        self.model = model
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        
        if PINECONE_INDEX_NAME not in [idx.name for idx in self.pc.list_indexes()]:
            self.pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=1024, 
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            # Wait for index to be ready
            import time
            while not self.pc.describe_index(PINECONE_INDEX_NAME).status['ready']:
                time.sleep(1)
                
        self.index = self.pc.Index(PINECONE_INDEX_NAME)

    def upload_documents(self, documents):
        try:
            self.index.delete(delete_all=True)
        except Exception as e:
            # If the index is empty, some Pinecone configs might throw an error
            print(f"Skipping delete_all: {e}")
            
        embeddings = self.model.encode(documents)
        
        vectors = []
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            vectors.append({
                "id": f"vec_{i}",
                "values": emb.tolist(),
                "metadata": {"text": doc}
            })
        
        self.index.upsert(vectors=vectors)

    def search(self, query, k=3):
        query_embedding = self.model.encode([query]).tolist()
        results = self.index.query(vector=query_embedding, top_k=k, include_metadata=True)
        
        return [{
            "text": match["metadata"]["text"],
            "score": match["score"]
        } for match in results["matches"]]
