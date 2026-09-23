import os
import requests


ANALYZER_URL = os.getenv(
    "CODEGUARD_ANALYZER_URL",
    "http://127.0.0.1:5000/analyze"
)


def analyze_code(code, language):
    response = requests.post(
        ANALYZER_URL,
        json={
            "code": code,
            "language": language
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()


def review_code(code, language):

    result = analyze_code(
        code,
        language
    )

    return {
        "language": language,
        "risk": result.get("risk"),
        "suppressed": result.get(
            "suppressed",
            False
        ),
        "recommendation": result.get(
            "recommendation"
        ),
        "matched_pattern": result.get(
            "matched_pattern"
        ),
        "remediation_advisor": result.get(
            "remediation_advisor",
            {}
        )
    }


def print_review(result):

    print("\n===================================")
    print("       CODEGUARD AI REVIEW")
    print("===================================")

    print("Language:", result["language"])
    print("Risk:", result["risk"])
    print("Suppressed:", result["suppressed"])

    print("\nRecommendation:")

    if result["recommendation"]:
        print(result["recommendation"])
    else:
        print("No remediation recommendation.")

    print("\nMatched Pattern:")
    print(result["matched_pattern"])

    print("\n===================================")


if __name__ == "__main__":

    sample_code = """
int timestamp = time(NULL);
"""

    result = review_code(
        sample_code,
        "C"
    )

    print_review(result)