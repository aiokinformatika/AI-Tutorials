from pathlib import Path
import pymupdf

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_document(path: Path) -> list[dict]:
    """Return a list of {text, page} records; page starts at 1 for PDFs."""
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Only PDF, TXT, and Markdown files are supported.")
    if suffix == ".pdf":
        with pymupdf.open(path) as document:
            pages = [
                {"text": page.get_text("text", sort=True).strip(), "page": i + 1}
                for i, page in enumerate(document)
            ]
        pages = [p for p in pages if p["text"]]
        if not pages:
            raise ValueError("No selectable text found in PDF (scanned PDFs need OCR).")
        return pages

    text = path.read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError("The document is empty.")
    return [{"text": text, "page": 0}]
