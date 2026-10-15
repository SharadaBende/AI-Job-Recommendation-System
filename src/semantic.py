import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from src.clean import load_clean_jobs

MODEL_NAME = "all-MiniLM-L6-v2"
CACHE = Path("data/job_embeddings.npz")

jobs = load_clean_jobs()
jobs["text"] = jobs["title_clean"] + ". " + jobs["description_clean"]
model = SentenceTransformer(MODEL_NAME)


def _load_embeddings():
    ids = jobs["id"].to_numpy(dtype=str)
    if CACHE.exists():
        cached = np.load(CACHE, allow_pickle=False)
        if np.array_equal(cached["ids"], ids):
            return cached["emb"]          # reuse, jobs haven't changed
    emb = model.encode(
        jobs["text"].tolist(),
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True,
    )
    np.savez(CACHE, ids=ids, emb=emb)
    return emb


job_emb = _load_embeddings()


def recommend(resume_text, k=10):
    q = model.encode([resume_text], normalize_embeddings=True)
    scores = job_emb @ q[0]               # cosine similarity (vectors are normalized)
    top = scores.argsort()[::-1][:k]
    out = jobs.iloc[top][["title_clean", "company", "location", "url"]].copy()
    out["score"] = scores[top].astype(float).round(3)
    return out


if __name__ == "__main__":
    from src.baseline import SAMPLE_RESUME, recommend as tfidf_recommend

    sem = recommend(SAMPLE_RESUME)
    for i, (_, r) in enumerate(sem.iterrows(), 1):
        print(f"{i}. {r['title_clean']} | {r['company']} | {r['location']} | score {r['score']}")
        print(f"   {r['url']}")

    overlap = set(sem["url"]) & set(tfidf_recommend(SAMPLE_RESUME)["url"])
    print(f"\nOverlap with TF-IDF top 10: {len(overlap)} of 10")