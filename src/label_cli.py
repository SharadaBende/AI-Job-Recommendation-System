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
print(f"{len(todo)} left to label. Enter 0, 1 or 2 (s = skip, q = save and quit)\n")

for idx, r in todo.iterrows():
    print("-" * 70)
    print(f"PERSONA: {r['persona']}  ({PERSONAS[r['persona']]})")
    print(f"JOB:     {r['title']} | {r['company']} | {r['location']}")
    print(f"SNIPPET: {r['snippet']}")
    while True:
        a = input("score (0/1/2, s, q): ").strip().lower()
        if a in ("0", "1", "2"):
            df.loc[idx, "relevance"] = int(a)
            break
        if a == "s":
            break
        if a == "q":
            df.to_csv(PATH, index=False, encoding="utf-8-sig")
            print("Saved. Run again to continue.")
            raise SystemExit
    df.to_csv(PATH, index=False, encoding="utf-8-sig")   # save after every answer

print("Done. All rows labeled.")