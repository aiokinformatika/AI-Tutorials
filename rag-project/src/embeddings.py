import requests
from config import EMBEDDING_MODEL, OLLAMA_BASE_URL


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate local vectors through Ollama's /api/embed endpoint."""
    if not texts:
        return []
    response = requests.post(
        f"{OLLAMA_BASE_URL}/embed",
        json={"model": EMBEDDING_MODEL, "input": texts},
        timeout=180,
    )
    response.raise_for_status()
    vectors = response.json()["embeddings"]
    if len(vectors) != len(texts):
        raise RuntimeError("Ollama returned an unexpected number of embeddings.")
    return vectors
