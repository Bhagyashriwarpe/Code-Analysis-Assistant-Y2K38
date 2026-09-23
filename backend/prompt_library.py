import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET = os.path.join(BASE_DIR, "Y2038_Week1_Dataset_500_Unique_With_Recommendations.xlsx")
OUTPUT = os.path.join(BASE_DIR, "prompt_library.json")


def build_prompt_library(limit=50):
    import pandas as pd
    df = pd.read_excel(DATASET)
    df = df.drop_duplicates(subset=["Pattern", "Language", "Risk"])
    prompts = []
    templates = [
        "Analyze this {language} code for Year 2038 timestamp risk: {pattern}",
        "Explain the Y2038 risk in this {language} pattern and provide a safe remediation: {pattern}",
        "Review this {language} timestamp handling for 32-bit overflow: {pattern}",
        "Suggest an idiomatic post-2038-safe fix for this {language} code: {pattern}",
        "Classify the risk and explain the remediation rationale for this {language} pattern: {pattern}",
    ]
    for _, row in df.iterrows():
        for template in templates:
            prompts.append({
                "language": str(row["Language"]),
                "risk": str(row["Risk"]),
                "pattern": str(row["Pattern"]),
                "prompt": template.format(language=row["Language"], pattern=row["Pattern"]),
                "source": str(row.get("Source", "")),
            })
            if len(prompts) >= limit:
                break
        if len(prompts) >= limit:
            break
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    return prompts


if __name__ == "__main__":
    print(f"Generated {len(build_prompt_library())} prompts: {OUTPUT}")
