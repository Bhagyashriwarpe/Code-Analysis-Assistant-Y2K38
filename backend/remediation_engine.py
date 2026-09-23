import json
import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_FILE = os.path.join(BASE_DIR, "remediation_rules.json")


def _load_rules():
    with open(RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


RULES = _load_rules()


class ContextAwareRemediationEngine:
    """Data-driven remediation layer over the existing analyzer and KB."""

    def __init__(self, advisor, analyzer):
        self.advisor = advisor
        self.analyzer = analyzer

    def _find_rule(self, code, language):
        for rule in RULES:
            if rule["language"].lower() != str(language).lower():
                continue
            if re.search(rule["pattern"], code, re.MULTILINE):
                return rule
        return None

    def _apply_rule(self, code, rule):
        pattern = re.compile(rule["pattern"], re.MULTILINE)

        def replace(match):
            values = match.groupdict()
            return rule["replacement"].format(**values)

        fixed = pattern.sub(replace, code, count=1)
        include = rule.get("required_include")
        if include and include not in fixed:
            lines = fixed.splitlines()
            insert_at = 0
            while insert_at < len(lines) and lines[insert_at].startswith("#include"):
                insert_at += 1
            lines.insert(insert_at, include)
            fixed = "\n".join(lines)
        return fixed

    def explain(self, original_code, fixed_code, language, before, after, advisor_result, rule):
        matches = advisor_result.get("results", [])
        recommendation = matches[0].get("recommendation") if matches else None
        source = matches[0].get("source") if matches else None
        explanation = {
            "summary": "The remediation changes the timestamp representation without changing the surrounding business logic.",
            "why_vulnerable": rule.get("reason") if rule else (recommendation or "The retrieved knowledge-base pattern indicates timestamp handling that requires review."),
            "technical_rationale": recommendation or "The knowledge base did not provide a more specific technical rationale.",
            "change_applied": "A data-driven remediation rule matched the submitted code." if rule else "No validated transformation rule matched the submitted code.",
            "risk_before": before,
            "risk_after": after,
            "risk_delta": f"{before} -> {after}",
            "source": source,
            "generated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z"
        }
        return explanation

    def remediate(self, code, language):
        original = str(code).strip()
        if not original:
            raise ValueError("Code cannot be empty.")
        if not str(language).strip():
            raise ValueError("Language cannot be empty.")

        advisor_result = self.advisor.recommend(original, language, 3)
        before = self.analyzer(original, language)

        if not advisor_result.get("relevant"):
            fixed = original
            rule = None
        else:
            rule = self._find_rule(original, language)
            fixed = self._apply_rule(original, rule) if rule else original

        after = self.analyzer(fixed, language)
        explanation = self.explain(
            original, fixed, language, before, after, advisor_result, rule
        )

        return {
            "original_code": original,
            "fixed_code": fixed,
            "explanation": explanation,
            "risk_delta": explanation["risk_delta"],
            "rule_id": rule.get("id") if rule else None,
            "advisor": advisor_result
        }
