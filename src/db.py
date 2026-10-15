import sqlite3
from pathlib import Path

DB_PATH = Path("data/jobs.db")

def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                source TEXT,
                title TEXT,
                company TEXT,
                location TEXT,
                description TEXT,
                salary_min REAL,
                salary_max REAL,
                url TEXT,
                posted_at TEXT,
                fetched_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

if __name__ == "__main__":
    init_db()
    print("Database ready.")