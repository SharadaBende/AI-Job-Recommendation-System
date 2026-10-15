from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.clean import load_clean_jobs

SAMPLE_RESUME = """
Final-year computer science student with experience in Python, SQL, pandas,
scikit-learn and machine learning. Built NLP projects using spaCy and
transformers, trained classification models, and created dashboards.
Interested in data scientist and machine learning engineer roles in Pune
or Bangalore.
"""

jobs = load_clean_jobs()
jobs["text"] = jobs["title_clean"] + " " + jobs["title_clean"] + " " + jobs["description_clean"]

vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2)
job_matrix = vectorizer.fit_transform(jobs["text"])


def recommend(resume_text, k=10):
    q = vectorizer.transform([resume_text])
    scores = cosine_similarity(q, job_matrix).ravel()
    top = scores.argsort()[::-1][:k]
    out = jobs.iloc[top][["title_clean", "company", "location", "url"]].copy()
    out["score"] = scores[top].round(3)
    return out


if __name__ == "__main__":
    results = recommend(SAMPLE_RESUME)
    for i, (_, r) in enumerate(results.iterrows(), 1):
        print(f"{i}. {r['title_clean']} | {r['company']} | {r['location']} | score {r['score']}")
        print(f"   {r['url']}")