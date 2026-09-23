import json
import os
import statistics
import time
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE_DIR, "remediation_metrics.json")


def benchmark(url="http://127.0.0.1:5000/remediate", samples=None):
    if samples is None:
        import pandas as pd
        dataset_path = os.path.join(BASE_DIR, "Y2038_Week1_Dataset_500_Unique_With_Recommendations.xlsx")
        df = pd.read_excel(dataset_path)
        df = df[df["Label"].astype(str).str.upper().eq("UNSAFE")].head(3)
        samples = [
            {"code": str(row["Pattern"]), "language": str(row["Language"])}
            for _, row in df.iterrows()
        ]
    times = []
    results = []
    for item in samples:
        start = time.perf_counter()
        response = requests.post(url, json=item, timeout=30)
        elapsed = time.perf_counter() - start
        response.raise_for_status()
        times.append(elapsed)
        results.append(response.json())
    report = {
        "samples": len(samples),
        "average_seconds": round(statistics.mean(times), 4) if times else None,
        "max_seconds": round(max(times), 4) if times else None,
        "under_2_seconds": bool(times) and max(times) < 2,
        "results": results,
    }
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return report



if __name__ == "__main__":
    print(json.dumps(benchmark(), indent=2))
