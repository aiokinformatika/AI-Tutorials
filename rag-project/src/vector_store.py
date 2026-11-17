import chromadb
from config import CHROMA_DIR, COLLECTION_NAME

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def save_chunks(ids: list[str], chunks: list[dict], vectors: list[list[float]], source: str) -> None:
    collection.upsert(
        ids=ids,
        documents=[chunk["text"] for chunk in chunks],
        embeddings=vectors,
        metadatas=[{"source": source, "page": chunk["page"]} for chunk in chunks],
    )


def search(vector: list[float], top_k: int) -> list[dict]:
    if collection.count() == 0:
        return []
    result = collection.query(
        query_embeddings=[vector],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": text, "source": meta["source"], "page": meta["page"], "distance": distance}
        for text, meta, distance in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]


def delete_source(source: str) -> None:
    collection.delete(where={"source": source})
