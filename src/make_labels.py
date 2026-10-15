import pandas as pd
from src.baseline import recommend as tfidf_rec
from src.semantic import recommend as sem_rec, jobs

PERSONAS = {
    "fresher_nlp": """Final-year computer science student with experience in Python, SQL,
    pandas, scikit-learn and machine learning. Built NLP projects using spaCy and
    transformers, trained classification models, and created dashboards.""",

    "data_analyst": """Data analyst with 2 years of experience. Strong in SQL, Excel,
    Tableau and Power BI. Uses Python and pandas for reporting, builds dashboards,
    and presents insights to business stakeholders.""",

    "senior_ml": """Senior machine learning engineer with 6 years of experience.
    Deploys models to production using PyTorch, Docker, AWS and MLOps pipelines.
    Has led a team and designed recommendation systems.""",

    "computer_vision": """Deep learning engineer with 3 years of experience in computer
    vision. Uses PyTorch, OpenCV and TensorFlow for object detection and image
    classification. Has worked on model optimization and deployment.""",

    "data_engineer": """Data engineer with 3 years of experience. Builds ETL pipelines
    with Spark, Airflow and SQL, works with AWS and data warehouses, and writes
    production Python code.""",
}

rows, sources = [], []
for name, text in PERSONAS.items():
    pooled = {}
    for method, rec in [("tfidf", tfidf_rec), ("semantic", sem_rec)]:
        for _, r in rec(text, k=10).iterrows():
            pooled.setdefault(r["url"], []).append(method)
    for url, methods in pooled.items():
        j = jobs[jobs["url"] == url].iloc[0]
        rows.append({
            "persona": name,
            "title": j["title_clean"],
            "company": j["company"],
            "location": j["location"],
            "snippet": j["description_clean"][:300].replace("\n", " "),
            "url": url,
            "relevance": "",
        })
        sources.append({"persona": name, "url": url, "found_by": "+".join(methods)})

labels = pd.DataFrame(rows).sample(frac=1, random_state=42)          # shuffle
labels = labels.sort_values("persona", kind="stable")
labels.to_csv("data/labels_todo.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(sources).to_csv("data/label_sources.csv", index=False)

print("Rows to label:", len(labels))
print(labels.groupby("persona").size())