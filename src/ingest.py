import requests
from src.db import get_conn, init_db

def fetch_remotive(search="data", limit=50):
    r = requests.get(
        "https://remotive.com/api/remote-jobs",
        params={"search": search, "limit": limit},
        timeout=30,
    )
    r.raise_for_status()
    jobs = []
    for j in r.json()["jobs"]:
        jobs.append({
            "id": f"remotive-{j['id']}",
            "source": "Remotive",
            "title": j["title"],
            "company": j["company_name"],
            "location": j.get("candidate_required_location"),
            "description": j["description"],
            "salary_min": None,
            "salary_max": None,
            "url": j["url"],
            "posted_at": j["publication_date"],
        })
    return jobs

def save(jobs):
    cols = ["id", "source", "title", "company", "location", "description",
            "salary_min", "salary_max", "url", "posted_at"]
    sql = f"INSERT OR REPLACE INTO jobs ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})"
    with get_conn() as conn:
        for job in jobs:
            conn.execute(sql, [job[c] for c in cols])
    return len(jobs)

if __name__ == "__main__":
    init_db()
    jobs = fetch_remotive("data")
    print("Saved from Remotive:", save(jobs))