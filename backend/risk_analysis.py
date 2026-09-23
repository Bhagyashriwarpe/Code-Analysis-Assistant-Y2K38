import math


def calculate_effort(risk, language="C", complexity="Moderate"):

    base_effort = {
        "CRITICAL": 5,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 0.5
    }

    technology_adjustment = {
        "C": 1,
        "C++": 1,
        "JAVA": 0.5,
        "DATABASE": 1,
        "LINUX": 1
    }

    complexity_multiplier = {
        "Simple": 1,
        "Moderate": 1.5,
        "Complex": 2
    }

    risk = risk.upper()
    language = language.upper()

    base = base_effort.get(risk, 2)
    adjustment = technology_adjustment.get(language, 0.5)
    multiplier = complexity_multiplier.get(complexity, 1.5)

    effort = base * multiplier + adjustment

    return {
        "engineering_days": round(effort, 1),
        "sprints": math.ceil(effort / 10),
        "resources": 1 if effort <= 5 else 2
    }


def calculate_priority(
    severity,
    business_impact,
    technical_risk,
    regulatory_risk
):

    score = (
        severity * 0.40 +
        business_impact * 0.25 +
        technical_risk * 0.20 +
        regulatory_risk * 0.15
    )

    if score >= 4:
        priority = "CRITICAL"
    elif score >= 3:
        priority = "HIGH"
    elif score >= 2:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return {
        "score": round(score, 2),
        "priority": priority
    }


def business_risk(risk):

    risk = risk.upper()

    if risk == "CRITICAL":
        return {
            "operational": "Potential major system failure or service disruption.",
            "financial": "High potential remediation and operational exposure.",
            "regulatory": "High audit and compliance concern."
        }

    if risk == "HIGH":
        return {
            "operational": "Potential application or timestamp processing failure.",
            "financial": "Potential remediation cost and business disruption.",
            "regulatory": "Potential audit and compliance concern."
        }

    if risk == "MEDIUM":
        return {
            "operational": "Limited operational impact is possible.",
            "financial": "Moderate technical remediation cost.",
            "regulatory": "May require tracking as technical risk."
        }

    return {
        "operational": "Low immediate operational impact.",
        "financial": "Low expected remediation exposure.",
        "regulatory": "Low immediate compliance concern."
    }