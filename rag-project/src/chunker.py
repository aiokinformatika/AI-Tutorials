def chunk_pages(pages: list[dict], size: int, overlap: int) -> list[dict]:
    """Split each page into overlapping word windows."""
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Chunk size must be positive and overlap smaller than size.")
    chunks = []
    step = size - overlap
    for page in pages:
        words = page["text"].split()
        for start in range(0, len(words), step):
            piece = words[start:start + size]
            if piece:
                chunks.append({"text": " ".join(piece), "page": page["page"]})
            if start + size >= len(words):
                break
    return chunks
