from fastapi import FastAPI

app = FastAPI(title="AI Job Recommender")


@app.get("/health")
def health():
    return {"status": "ok"}