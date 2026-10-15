from src.clean import load_clean_jobs

df = load_clean_jobs()

print("Total jobs:", len(df))

print("\n--- Top 10 job titles ---")
print(df["title_clean"].value_counts().head(10))

print("\n--- Top 10 locations ---")
print(df["location"].value_counts().head(10))

print("\n--- Top 10 companies ---")
print(df["company"].value_counts().head(10))

print("\n--- Salary (Adzuna jobs that have it) ---")
sal = df.dropna(subset=["salary_min"])
print("Jobs with salary:", len(sal), "of", len(df))
print(sal[["salary_min", "salary_max"]].describe().round(0))

print("\n--- Quick skill mentions (share of jobs) ---")
skills = ["python", "sql", "machine learning", "deep learning", "pytorch",
          "tensorflow", "aws", "docker", "spark", "tableau", "power bi", "nlp"]
text = df["description_clean"].str.lower()
for s in skills:
    print(f"{s:18} {text.str.contains(s).mean():.0%}")