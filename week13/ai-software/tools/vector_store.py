from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = None

    def create_store(self, texts):
        self.db = FAISS.from_texts(texts, self.embeddings)

    def add_text(self, text):
        if self.db:
            self.db.add_texts([text])
        else:
            self.create_store([text])

    def search(self, query, k=3):
        if not self.db:
            return []
        return self.db.similarity_search(query, k=k)