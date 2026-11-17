import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
CHROMA_DIR = BASE_DIR / "data" / "chroma"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434/api")
CHAT_MODEL = "mistral"
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "rag_documents_v1"
CHUNK_SIZE_WORDS = 350
CHUNK_OVERLAP_WORDS = 60
TOP_K = 4
MAX_FILE_MB = 10

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
