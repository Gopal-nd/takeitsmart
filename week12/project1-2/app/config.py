import os
from dotenv import load_dotenv

# Load .env from the project root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path=env_path, override=True)

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-index")

# Local Storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_DB_PATH = os.path.join(BASE_DIR, "faiss_index")
