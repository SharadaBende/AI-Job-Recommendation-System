import pandas as pd

PATH = "data/labels_done.csv"
PERSONAS = {
    "fresher_nlp": "Final-year student, Python/SQL/ML, NLP projects",
    "data_analyst": "2 yrs data analyst: SQL, Excel, Tableau, Power BI",
    "senior_ml": "6 yrs senior ML engineer: deployment, MLOps, team lead",
    "computer_vision": "3 yrs deep learning, computer vision, PyTorch/OpenCV",
    "data_engineer": "3 yrs data engineer: Spark, Airflow, ETL, AWS",
}

df = pd.read_csv(PATH, encoding="utf-8-sig")
todo = df[df["relevance"].isna()]
print(f"{len(todo)} left to label. Enter 0, 1 or 2 (q = save and quit)\n")

for n, (idx, r) in enumerate(todo.iterrows(), 1):
    print("-" * 70)
    print(f"[{n}/{len(todo)}] PERSONA: {r['persona']}  ({PERSONAS[r['persona']]})")
    print(f"JOB:     {r['title']} | {r['company']} | {r['location']}")
    print(f"SNIPPET: {r['snippet']}")
    while True:
        a = input("score (0/1/2, q): ").strip().lower()
        if a in ("0", "1", "2"):
            df.loc[idx, "relevance"] = int(a)
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            break
        if a == "q":
            left = df["relevance"].isna().sum()
            print(f"Saved. {left} still unlabeled. Run again to continue.")
            raise SystemExit
        print("Please type 0, 1 or 2.")

left = df["relevance"].isna().sum()
print("Done. All rows labeled." if left == 0 else f"{left} rows still unlabeled.")