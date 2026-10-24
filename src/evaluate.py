import numpy as np
import pandas as pd
from src.personas import PERSONAS
from src.baseline import recommend as tfidf_rec
from src.semantic import recommend as sem_rec

labels = pd.read_csv("data/labels_done.csv", encoding="utf-8-sig")
assert labels["relevance"].notna().all(), "Some rows are still unlabeled."


def dcg(rels):
    rels = np.asarray(rels, dtype=float)
    return float(((2 ** rels - 1) / np.log2(np.arange(2, len(rels) + 2))).sum())


def evaluate(rec, k=10):
    rows = []
    for name, text in PERSONAS.items():
        pool = labels[labels["persona"] == name].set_index("url")["relevance"]
        top = rec(text, k=k)["url"].tolist()
        rels = [pool.get(u, 0) for u in top]
        ideal = sorted(pool.tolist(), reverse=True)[:k]
        rows.append({
            "persona": name,
            "P@10 (good fit)": np.mean([r == 2 for r in rels]),
            "P@10 (partial+)": np.mean([r >= 1 for r in rels]),
            "NDCG@10": dcg(rels) / dcg(ideal) if dcg(ideal) > 0 else 0.0,
        })
    out = pd.DataFrame(rows).set_index("persona")
    out.loc["MEAN"] = out.mean()
    return out.round(3)


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)
    print("=== TF-IDF baseline ===")
    print(evaluate(tfidf_rec))
    print("\n=== Semantic (MiniLM embeddings) ===")
    print(evaluate(sem_rec))