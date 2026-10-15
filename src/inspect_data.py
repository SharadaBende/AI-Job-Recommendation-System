import sqlite3
import pandas as pd

df = pd.read_sql("SELECT * FROM jobs", sqlite3.connect("data/jobs.db"))

print("Shape:", df.shape)

print("\n--- Missing values ---")
print(df.isna().sum())

print("\n--- Description length (characters) by source ---")
df["desc_len"] = df["description"].str.len()
print(df.groupby("source")["desc_len"].describe()[["mean", "min", "max"]])

print("\n--- Sample Remotive description (first 300 chars) ---")
print(df[df.source == "Remotive"]["description"].iloc[0][:300])

print("\n--- Sample Adzuna description (first 300 chars) ---")
print(df[df.source == "Adzuna"]["description"].iloc[0][:300])