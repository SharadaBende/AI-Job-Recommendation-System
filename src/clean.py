import html
import re
import sqlite3
import pandas as pd


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>", "\n", text)  # keep line breaks
    text = re.sub(r"<[^>]+>", " ", text)                           # strip tags
    text = html.unescape(text)                                     # &amp; -> &
    text = re.sub(r"[ \t]+", " ", text)                            # collapse spaces
    text = re.sub(r"\n\s*\n+", "\n", text)                         # collapse blank lines
    return text.strip()


RELEVANT = re.compile(
    r"\bdata\b|machine learning|\bml\b|\bai\b|\bnlp\b|analytics|scientist|"
    r"deep learning|\bllm\b|computer vision|generative|\bgenai\b",
    re.IGNORECASE,
)


def load_clean_jobs():
    df = pd.read_sql("SELECT * FROM jobs", sqlite3.connect("data/jobs.db"))
    df["description_clean"] = df["description"].apply(clean_text)
    df["title_clean"] = df["title"].str.strip()

    # treat 0 salaries as missing
    for col in ["salary_min", "salary_max"]:
        df.loc[df[col] <= 0, col] = None

    # keep only relevant titles
    df = df[df["title_clean"].str.contains(RELEVANT)]

    df = df.drop_duplicates(subset=["title_clean", "company"])
    return df.reset_index(drop=True)

if __name__ == "__main__":
    raw = pd.read_sql("SELECT * FROM jobs", sqlite3.connect("data/jobs.db"))
    df = load_clean_jobs()
    print("Raw jobs:", len(raw), "-> After cleaning:", len(df))
    print("\nBy source:")
    print(df["source"].value_counts())
    print("\nSample of titles that were removed:")
    removed = raw[~raw["title"].str.strip().str.contains(RELEVANT)]
    print(removed["title"].head(15).to_string(index=False))