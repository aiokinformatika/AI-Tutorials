# Local RAG Project — Docker, Python, Ollama, Streamlit and Chroma

Companion project for [AI OKInformatika’s RAG tutorial](https://ai.okinformatika.si/2026/10/26/build-your-first-local-rag-system-chat-with-your-own-documents/tutorials/).

This is a **local, single-user educational project**. Do not expose it to untrusted networks.

## Prerequisites (host)

- Docker Engine and `docker compose` plugin installed, with permission to use Docker.
- Git (or an extracted project ZIP), terminal, and browser.
- Internet to download images, Python dependencies during build, and Ollama models.
- Recommended **16 GB RAM and 15 GB free disk** for this CPU-only example; these are practical estimates, not guaranteed minima.
- Free host TCP port `127.0.0.1:8501`. No Python, pip, venv, Ollama, or Chroma installation on the host.

**Security:** Docker daemon access is privileged. Run commands only on a machine where you trust the Docker installation and the images. Data and models persist locally. Avoid sensitive documents for a public tutorial.

## Run

From `AI-Tutorials/rag-project`:

```bash
docker --version
docker compose version
docker compose config -q
docker compose build app
docker compose up -d ollama
docker compose exec ollama ollama pull mistral
docker compose exec ollama ollama pull nomic-embed-text
docker compose exec ollama ollama list
docker compose run --rm --no-deps app python -m pip check
docker compose run --rm --no-deps app python -m compileall -q app.py config.py src tests
docker compose run --rm --no-deps app python -m unittest discover -s tests -v
docker compose up -d app
docker compose ps
```

Open <http://127.0.0.1:8501> and upload `tests/company_policy.txt`.

- Ask `How many vacation days do employees receive?` (document says 25 per calendar year).
- Ask `Who approves expense reports?` (finance manager).
- Ask `Who provides health insurance?` (document does not say; inspect the response).
- Verify the retrieved passages, restart app with `docker compose restart app`, and ask again.

View logs: `docker compose logs --tail=100 app ollama`.
Stop without deleting stored data/models: `docker compose down`.

**Never use `docker compose down -v` as routine cleanup**: it removes the `ollama_models` volume and model downloads. The host `./data/` directory contains your uploads and Chroma index; back it up before deliberate deletion.

## Architecture

- `compose.yaml`: two services. `app` is the Streamlit/Python application. `ollama` serves both AI models on the *internal* Docker network.
- `Dockerfile`: Python 3.12 and the application's Python dependencies **inside the image**.
- `config.py`: document paths, model names, chunk sizes, retrieval and API URL; `OLLAMA_BASE_URL` reads Compose's environment variable.
- `src/document_loader.py`: PDF/TXT/MD extraction, `src/chunker.py`: overlapping chunks, `src/embeddings.py`: Ollama `/api/embed`, `src/vector_store.py`: embedded persistent Chroma, `src/llm.py`: Ollama `/api/chat`, `src/rag.py`: orchestration, `app.py`: UI.
- `./data:/app/data`: host-mounted uploads and Chroma index (retained across container rebuilds).
- `ollama_models:/root/.ollama`: Docker named volume for downloaded models.
- Only Streamlit is published on host loopback (`127.0.0.1:8501`). Port `11434` is **not** exposed to host.

The two containers share a Docker network. Inside `app`, `localhost` means the **app container**, so the Ollama API URL is `http://ollama:11434/api`, not `http://127.0.0.1:11434/api`.

## Configuration settings

See `config.py` and the blog article. Defaults: `CHAT_MODEL=mistral`, `EMBEDDING_MODEL=nomic-embed-text`, `COLLECTION_NAME=rag_documents_v1`, `CHUNK_SIZE_WORDS=350`, `CHUNK_OVERLAP_WORDS=60`, `TOP_K=4`, `MAX_FILE_MB=10`.

Changing the embedding model requires a **new collection** and reindexing; changing chunk size/overlap also requires reindexing. No user authentication, OCR, or DOCX support is included.

## Verification status

Run automated checks **inside the container** as shown. Mock-based tests do not prove complete Ollama/Chroma/Streamlit behavior; manually verify upload → index → retrieval → answer and record results before publication. Package version ranges are not a lockfile.
