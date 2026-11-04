from fastapi import FastAPI

app = FastAPI(
    title="AI Tutorials - Docker Test",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Docker and FastAPI are working!",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
