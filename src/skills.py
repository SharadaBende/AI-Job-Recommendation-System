import re

SKILLS = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "spark": ["spark", "pyspark"],
    "airflow": ["airflow"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "sagemaker"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "tableau": ["tableau"],
    "power bi": ["power bi", "powerbi"],
    "excel": ["excel"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "opencv"],
    "llm": ["llm", "large language model"],
    "transformers": ["transformers", "bert"],
    "spacy": ["spacy"],
    "mlflow": ["mlflow"],
    "fastapi": ["fastapi"],
    "git": ["git", "github"],
    "hadoop": ["hadoop"],
    "etl": ["etl"],
    "databricks": ["databricks"],
    "machine learning": ["machine learning"],
    "deep learning": ["deep learning"],
    "statistics": ["statistics", "statistical"],
    "rag": ["rag", "retrieval augmented"],
}


def extract_skills(text):
    text = (text or "").lower()
    found = set()
    for skill, aliases in SKILLS.items():
        for a in aliases:
            if re.search(r"(?<![a-z0-9])" + re.escape(a) + r"(?![a-z0-9])", text):
                found.add(skill)
                break
    return found


def compare(resume_text, job_text):
    have = extract_skills(resume_text)
    need = extract_skills(job_text)
    return sorted(have & need), sorted(need - have)


if __name__ == "__main__":
    resume = "I know Python, SQL and pandas. Built NLP projects with spaCy."
    job = "Need Python, SQL, Docker, AWS and Airflow."
    matched, missing = compare(resume, job)
    print("matched:", matched)
    print("missing:", missing)