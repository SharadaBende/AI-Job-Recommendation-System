import re
import pandas as pd

PATH = "data/labels_done.csv"

# keywords for the persona's field, and the experience range (years) they fit
CONFIG = {
    "fresher_nlp":     (["nlp", "natural language", "text mining", "llm", "transformer", "bert", "language model"], (0, 2)),
    "data_analyst":    (["data analyst", "sql", "tableau", "power bi", "excel", "dashboard", "reporting", "business intelligence"], (1, 4)),
    "senior_ml":       (["machine learning", "mlops", "deploy", "production", "model serving", "ml platform"], (5, 15)),
    "computer_vision": (["computer vision", "opencv", "image", "object detection", "vision", "cnn"], (2, 5)),
    "data_engineer":   (["spark", "airflow", "etl", "pipeline", "data engineer", "warehouse", "pyspark"], (2, 5)),
}
SENIOR = re.compile(r"\b(senior|sr\.?|lead|principal|staff|head)\b", re.I)
JUNIOR = re.compile(r"\b(intern|internship|junior|fresher|trainee|graduate)\b", re.I)
YEARS = re.compile(r"(\d+)\s*(?:\+|-|–|to)?\s*\d*\s*\+?\s*(?:years|year|yrs|yr)", re.I)


def suggest(row):
    kws, (lo, hi) = CONFIG[row["persona"]]
    title, text = str(row["title"]), f"{row['title']} {row['snippet']}".lower()
    hits = sum(k in text for k in kws)

    m = YEARS.findall(str(row["snippet"]))
    if m:
        job_lo = min(int(x) for x in m)
        level_ok = lo - 1 <= job_lo <= hi + 1
    elif SENIOR.search(title):
        level_ok = lo >= 4
    elif JUNIOR.search(title):
        level_ok = hi <= 3
    else:
        level_ok = True          # unknown level: give benefit of the doubt

    if hits >= 2 and level_ok:
        return 2
    if (hits >= 2 and not level_ok) or (hits == 1 and level_ok):
        return 1
    return 0


df = pd.read_csv(PATH, encoding="utf-8-sig")
if "suggested" not in df.columns:
    df["suggested"] = df.apply(suggest, axis=1)
todo = df[df["relevance"].isna()]
print(f"{len(todo)} to review. Enter = accept suggestion, 0/1/2 = override, q = save & quit\n")

for n, (idx, r) in enumerate(todo.iterrows(), 1):
    print("-" * 70)
    print(f"[{n}/{len(todo)}] PERSONA: {r['persona']}")
    print(f"JOB:     {r['title']} | {r['company']} | {r['location']}")
    print(f"SNIPPET: {r['snippet']}")
    while True:
        a = input(f"suggested = {int(r['suggested'])}  ->  ").strip().lower()
        if a == "":
            df.loc[idx, "relevance"] = int(r["suggested"])
        elif a in ("0", "1", "2"):
            df.loc[idx, "relevance"] = int(a)
        elif a == "q":
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            print(f"Saved. {df['relevance'].isna().sum()} still unlabeled.")
            raise SystemExit
        else:
            print("Press Enter, or type 0, 1, 2, q.")
            continue
        df.to_csv(PATH, index=False, encoding="utf-8-sig")
        break

print(f"Done. Unlabeled rows left: {df['relevance'].isna().sum()}")