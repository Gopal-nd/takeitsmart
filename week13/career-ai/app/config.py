import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "faiss_store")

def validate_config():
    if not GROQ_API_KEY:
        raise ValueError("❌ GROQ_API_KEY not found in .env")
