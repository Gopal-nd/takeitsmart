import os
from dotenv import load_dotenv

# Load .env from the project root
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
load_dotenv(dotenv_path=env_path, override=True)

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# MySQL
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "gopal@2005"),
    "database": os.getenv("DB_NAME", "rag_company")
}

# Storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "vectorstore/faiss_index")
