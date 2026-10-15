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


def load_clean_jobs():
    df = pd.read_sql("SELECT * FROM jobs", sqlite3.connect("data/jobs.db"))
    df["description_clean"] = df["description"].apply(clean_text)
    df["title_clean"] = df["title"].str.strip()
    df = df.drop_duplicates(subset=["title_clean", "company"])
    return df.reset_index(drop=True)


if __name__ == "__main__":
    df = load_clean_jobs()
    print("Jobs after dedupe:", len(df))
    r = df[df.source == "Remotive"].iloc[0]
    print("\n--- Remotive BEFORE ---")
    print(r["description"][:200])
    print("\n--- Remotive AFTER ---")
    print(r["description_clean"][:200])
    print("\nAvg clean length by source:")
    print(df.groupby("source")["description_clean"].apply(lambda s: s.str.len().mean()))