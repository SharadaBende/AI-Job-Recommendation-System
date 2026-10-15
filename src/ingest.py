import os
import requests
from dotenv import load_dotenv
from src.db import get_conn, init_db

load_dotenv()


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


def fetch_adzuna(what="data scientist", country="in", pages=2):
    app_id = os.getenv("ADZUNA_APP_ID")
    app_key = os.getenv("ADZUNA_APP_KEY")
    jobs = []
    for page in range(1, pages + 1):
        r = requests.get(
            f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
            params={"app_id": app_id, "app_key": app_key,
                    "what": what, "results_per_page": 50},
            timeout=30,
        )
        r.raise_for_status()
        for j in r.json()["results"]:
            jobs.append({
                "id": f"adzuna-{j['id']}",
                "source": "Adzuna",
                "title": j["title"],
                "company": j.get("company", {}).get("display_name"),
                "location": j.get("location", {}).get("display_name"),
                "description": j["description"],
                "salary_min": j.get("salary_min"),
                "salary_max": j.get("salary_max"),
                "url": j["redirect_url"],
                "posted_at": j["created"],
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
    print("Adzuna:", save(fetch_adzuna("data scientist")))