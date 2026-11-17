import hashlib
from pathlib import Path
import streamlit as st
from config import MAX_FILE_MB, UPLOAD_DIR
from src.rag import ask, index_document

st.set_page_config(page_title="Local RAG Project", page_icon="📄")
st.title("Chat with your documents")
st.caption("Streamlit + Chroma + Ollama + Mistral")

uploads = st.file_uploader(
    "Choose PDF, TXT or Markdown documents",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True,
)

if st.button("Index uploaded documents", disabled=not uploads):
    for uploaded in uploads or []:
        try:
            contents = uploaded.getvalue()
            if not contents or len(contents) > MAX_FILE_MB * 1024 * 1024:
                raise ValueError(f"Each file must be between 1 byte and {MAX_FILE_MB} MB.")
            extension = Path(uploaded.name).suffix.lower()
            if extension not in {".pdf", ".txt", ".md"}:
                raise ValueError("Unsupported file extension.")
            # Safe, app-generated filename; never trust uploader paths.
            digest = hashlib.sha256(contents).hexdigest()[:16]
            destination = UPLOAD_DIR / f"{digest}{extension}"
            destination.write_bytes(contents)
            count = index_document(destination, uploaded.name)
            st.success(f"Indexed {uploaded.name}: {count} chunks")
        except Exception as exc:
            st.error(f"Could not index {uploaded.name}: {exc}")

question = st.chat_input("Ask a question about your documents")
if question:
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Searching documents and generating answer..."):
                answer, sources = ask(question)
            st.write(answer)
            if sources:
                with st.expander("Retrieved sources (verify the answer)"):
                    for item in sources:
                        page = f", page {item['page']}" if item["page"] else ""
                        st.write(f"Source: {item['source']}{page}")
                        st.write(item["text"])
        except Exception as exc:
            st.error(f"Request failed: {exc}")
