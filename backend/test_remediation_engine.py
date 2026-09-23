from remediation_engine import ContextAwareRemediationEngine


class MockAdvisor:
    def recommend(self, code, language, top_k):
        return {
            "relevant": True,
            "results": [{
                "recommendation": "Use a verified 64-bit timestamp representation.",
                "source": "Knowledge Base"
            }]
        }


def mock_analyzer(code, language):
    return "HIGH" if "int timestamp" in code or "int unixTime" in code or "int created" in code else "LOW"


def run():
    engine = ContextAwareRemediationEngine(MockAdvisor(), mock_analyzer)
    cases = [
        ("C", "int timestamp = time(NULL);"),
        ("C++", "int created=time(NULL);"),
        ("Java", "int unixTime = (int)(System.currentTimeMillis()/1000);"),
    ]
    for language, code in cases:
        result = engine.remediate(code, language)
        assert result["fixed_code"] != code
        assert result["risk_delta"].endswith("-> LOW")
    print("Remediation engine tests passed.")


if __name__ == "__main__":
    run()
