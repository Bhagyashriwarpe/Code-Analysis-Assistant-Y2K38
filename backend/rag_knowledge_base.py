import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET = os.path.join(
    BASE_DIR,
    "Y2038_Week1_Dataset_500_Unique_With_Recommendations.xlsx"
)


def load_knowledge_base():
    df = pd.read_excel(DATASET)

    records = []

    for _, row in df.iterrows():
        records.append({
            "pattern": str(row.get("Pattern", "")),
            "language": str(row.get("Language", "")),
            "risk": str(row.get("Risk", "")),
            "label": str(row.get("Label", "")),
            "recommendation": str(row.get("Recommendation", "")),
            "source": str(row.get("Source", "")),
            "source_url": str(row.get("Source URL", ""))
        })

    return records


KNOWLEDGE_BASE = load_knowledge_base()


def search_knowledge(query, language=None, top_k=3):

    query_words = set(
        re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", query.lower())
    )

    results = []

    for item in KNOWLEDGE_BASE:

        if language and item["language"].lower() != language.lower():
            continue

        text = (
            item["pattern"] + " " +
            item["recommendation"] + " " +
            item["risk"] + " " +
            item["label"]
        ).lower()

        score = sum(1 for word in query_words if word in text)

        if score > 0:
            results.append((score, item))

    results.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in results[:top_k]]