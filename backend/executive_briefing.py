def build_briefing(findings):
    findings = findings or []
    counts = {}
    total_effort = 0.0
    for item in findings:
        risk = str(item.get("risk", "LOW")).upper()
        counts[risk] = counts.get(risk, 0) + 1
        total_effort += float(item.get("effort", {}).get("engineering_days", 0))
    ordered = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    return {
        "finding_count": len(findings),
        "risk_distribution": dict(ordered),
        "estimated_engineering_days": round(total_effort, 1),
        "briefing": "Assessment results are summarized from the submitted findings, risk classification and remediation-effort estimates."
    }
