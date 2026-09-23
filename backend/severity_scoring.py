import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(BASE_DIR, "severity_scoring.json")


def score_finding(severity, reachability=1, production_exposure=1, persistence=1, external_dependency=1):
    with open(CONFIG, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    sev = cfg["severity_values"].get(str(severity).upper(), cfg["severity_values"]["LOW"])
    factors = {
        "severity": sev,
        "reachability": float(reachability),
        "production_exposure": float(production_exposure),
        "persistence": float(persistence),
        "external_dependency": float(external_dependency)
    }
    score = sum(factors[k] * cfg["weights"][k] for k in factors)
    thresholds = cfg["thresholds"]
    if score >= thresholds["critical"]: level = "CRITICAL"
    elif score >= thresholds["high"]: level = "HIGH"
    elif score >= thresholds["medium"]: level = "MEDIUM"
    else: level = "LOW"
    return {"score": round(score, 2), "severity": level, "factors": factors}
