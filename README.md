# AI Job Recommendation System

Paste a resume or short profile and get matching jobs from India, with the skills you already have and the skills you are missing for each job.

## What it does
- Collects real job postings from the Adzuna and Remotive APIs
- Cleans the text and stores it in SQLite
- Ranks jobs by meaning (sentence embeddings), not just matching words
- Filters by city and maximum years of experience
- Shows matched and missing skills for every result

## How it works
```
Job APIs -> clean text -> SQLite -> embeddings (MiniLM) -> semantic search -> filters -> skill match -> Streamlit app
```

## Results
Evaluated on 5 candidate profiles and 84 hand-labeled jobs (0 = not a fit, 1 = partial, 2 = good fit).

| Method | Good fits in top 10 | Good or partial fits in top 10 | NDCG@10 |
|---|---|---|---|
| TF-IDF baseline | 0.36 | 0.80 | 0.633 |
| **Semantic search (used)** | **0.44** | **0.94** | **0.769** |
| Semantic + re-ranker (level + location) | 0.44 | 0.72 | 0.676 |

Semantic search beat the keyword baseline on average, mostly because it found NLP jobs that TF-IDF missed.
The re-ranker did not beat plain semantic search on this test, so city and experience are applied as optional filters instead.

## Limitations
- Small evaluation set (5 profiles, 84 labels), so the results are a good sign and not proof.
- The labels were first suggested by simple rules and then reviewed and corrected by hand.
- The labeled jobs came from the top results of the TF-IDF and semantic models, so the test favors those two.
- Adzuna job descriptions are cut off at 500 characters, so skill matching only sees part of each posting.
- The seniority check only works when the posting states years of experience.

## Run it
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
# add your Adzuna keys to a .env file:
# ADZUNA_APP_ID=...
# ADZUNA_APP_KEY=...
python -m src.ingest
streamlit run app.py
```

## Data sources
Jobs come from [Adzuna](https://developer.adzuna.com/) and [Remotive](https://remotive.com/). Each result links back to the original posting.

## Tech
Python, pandas, SQLite, scikit-learn, sentence-transformers, Streamlit