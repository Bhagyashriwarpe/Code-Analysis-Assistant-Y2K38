from review_bot import review_code


changed_files = [
    {
        "filename": "example.c",
        "code": """
int timestamp = time(NULL);
"""
    },
    {
        "filename": "example.java",
        "code": """
long timestamp = System.currentTimeMillis();
"""
    },
    {
        "filename": "example.c",
        "code": """
int count = 100;
"""
    }
]


def detect_language(filename):

    extension = filename.split(".")[-1].lower()

    languages = {
        "c": "C",
        "cpp": "C++",
        "cc": "C++",
        "java": "Java"
    }

    return languages.get(extension)


for file in changed_files:

    language = detect_language(
        file["filename"]
    )

    result = review_code(
        file["code"],
        language
    )

    print("\n===================================")
    print("FILE:", file["filename"])
    print("LANGUAGE:", language)
    print("RISK:", result["risk"])
    print("SUPPRESSED:", result["suppressed"])
    print(
        "RECOMMENDATION:",
        result["recommendation"]
    )
    print(
        "MATCHED PATTERN:",
        result["matched_pattern"]
    )
    print("===================================")