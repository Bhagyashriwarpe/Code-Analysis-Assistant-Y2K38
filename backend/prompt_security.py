import re

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]+"),
    re.compile(r"(?i)-----BEGIN [A-Z ]+-----.*?-----END [A-Z ]+-----", re.DOTALL),
]


def sanitize_prompt(text):
    value = str(text or "")
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED]", value)
    value = re.sub(r"(?i)\b(?:customer|client|company|tenant)[_-]?[A-Za-z0-9.-]+", "[REDACTED_NAME]", value)
    return value
