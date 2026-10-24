from src.semantic import recommend as sem_rec, jobs
from src.features import job_years


def search(resume_text, k=10, cities=None, max_years=None):
    """Semantic search, then optional filters on city and experience."""
    results = sem_rec(resume_text, k=100)
    keep = []
    for _, r in results.iterrows():
        j = jobs[jobs["url"] == r["url"]].iloc[0]
        if cities:
            loc = (j["location"] or "").lower()
            if not any(c.lower() in loc for c in cities):
                continue
        if max_years is not None:
            yrs = job_years(j["title_clean"], j["description_clean"])
            if yrs is not None and yrs > max_years:
                continue
        r["description"] = j["description_clean"]
        keep.append(r)
        if len(keep) == k:
            break
    return keep


if __name__ == "__main__":
    from src.baseline import SAMPLE_RESUME
    for i, r in enumerate(search(SAMPLE_RESUME, cities=["Pune"], max_years=2), 1):
        print(f"{i}. {r['title_clean']} | {r['company']} | {r['location']} | {r['score']}")