from src.semantic import recommend as sem_rec, jobs
from src.features import job_years, level_match, location_match

W_SEM, W_LEVEL, W_LOC = 0.85, 0.15, 0.0


def recommend(resume_text, candidate_years=0, wanted=("pune", "bangalore"), k=10, pool=50):
    cands = sem_rec(resume_text, k=pool).copy()
    rows = []
    for _, r in cands.iterrows():
        j = jobs[jobs["url"] == r["url"]].iloc[0]
        yrs = job_years(j["title_clean"], j["description_clean"])
        lvl = level_match(candidate_years, yrs)
        loc = location_match(list(wanted), j["location"])
        rows.append(W_SEM * r["score"] + W_LEVEL * lvl + W_LOC * loc)
    cands["final"] = rows
    cands = cands.sort_values("final", ascending=False).head(k)
    cands["score"] = cands["final"].round(3)
    return cands[["title_clean", "company", "location", "url", "score"]]


if __name__ == "__main__":
    from src.baseline import SAMPLE_RESUME
    res = recommend(SAMPLE_RESUME, candidate_years=0)
    for i, (_, r) in enumerate(res.iterrows(), 1):
        print(f"{i}. {r['title_clean']} | {r['company']} | {r['location']} | {r['score']}")