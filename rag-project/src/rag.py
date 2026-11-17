import hashlib
from pathlib import Path
from config import CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS, TOP_K
from src.document_loader import load_document
from src.chunker import chunk_pages
from src.embeddings import embed_texts
from src.vector_store import delete_source, save_chunks, search
from src.llm import answer_question


def index_document(path: Path, display_name: str) -> int:
    pages = load_document(path)
    chunks = chunk_pages(pages, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS)
    vectors = embed_texts([chunk["text"] for chunk in chunks])
    document_hash = hashlib.sha256(display_name.encode("utf-8")).hexdigest()[:16]
    ids = [f"{document_hash}-{i}" for i in range(len(chunks))]
    # Do not remove the previous index until extraction/embedding succeeded.
    delete_source(display_name)
    save_chunks(ids, chunks, vectors, display_name)
    return len(chunks)


def ask(question: str) -> tuple[str, list[dict]]:
    retrieved = search(embed_texts([question])[0], TOP_K)
    if not retrieved:
        return "No indexed documents available. Upload a document first.", []
    context = "\n\n".join(
        f"[Source {i}: {item['source']}, page {item['page'] or 'N/A'}]\n{item['text']}"
        for i, item in enumerate(retrieved, 1)
    )
    return answer_question(question, context), retrieved
