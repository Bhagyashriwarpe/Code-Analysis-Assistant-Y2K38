import os
import json
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECOMMENDATION_DATASET = os.path.join(
    BASE_DIR,
    "recommendation_dataset.pkl"
)

FALSE_POSITIVE_MODEL = os.path.join(
    BASE_DIR,
    "false_positive_model.pkl"
)

FALSE_POSITIVE_VECTORIZER = os.path.join(
    BASE_DIR,
    "false_positive_vectorizer.pkl"
)

FEEDBACK_FILE = os.path.join(
    BASE_DIR,
    "remediation_feedback.json"
)


class RemediationAdvisorV2:

    def __init__(self):

        # Load recommendation knowledge base
        self.dataset = joblib.load(RECOMMENDATION_DATASET)

        if not isinstance(self.dataset, pd.DataFrame):
            raise TypeError(
                "recommendation_dataset.pkl must contain a pandas DataFrame."
            )

        required_columns = {
            "Pattern",
            "Language",
            "Risk",
            "Recommendation",
            "input_text"
        }

        missing_columns = (
            required_columns - set(self.dataset.columns)
        )

        if missing_columns:
            raise ValueError(
                "Missing dataset columns: " +
                ", ".join(sorted(missing_columns))
            )

        self.dataset = self.dataset.copy()

        self.dataset["input_text"] = (
            self.dataset["input_text"]
            .fillna("")
            .astype(str)
        )

        self.dataset["Language"] = (
            self.dataset["Language"]
            .fillna("")
            .astype(str)
        )

        self.dataset["Risk"] = (
            self.dataset["Risk"]
            .fillna("")
            .astype(str)
        )

        # TF-IDF remediation similarity model
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            token_pattern=r"(?u)\b\w+\b"
        )

        self.pattern_vectors = self.vectorizer.fit_transform(
            self.dataset["input_text"]
        )

        # Existing false-positive classifier
        self.false_positive_model = joblib.load(
            FALSE_POSITIVE_MODEL
        )

        self.false_positive_vectorizer = joblib.load(
            FALSE_POSITIVE_VECTORIZER
        )

        # Load audit feedback if available
        self.feedback = self._load_feedback()

    def _load_feedback(self):

        if not os.path.exists(FEEDBACK_FILE):
            return []

        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

        except (json.JSONDecodeError, OSError):
            pass

        return []

    def add_feedback(
        self,
        code,
        language,
        accepted_recommendation,
        corrected_recommendation=None,
        edge_case=None
    ):
        """
        Store client/audit feedback for future advisor improvement.
        """

        feedback_item = {
            "code": str(code),
            "language": str(language),
            "accepted_recommendation": bool(
                accepted_recommendation
            ),
            "corrected_recommendation": (
                str(corrected_recommendation)
                if corrected_recommendation
                else ""
            ),
            "edge_case": (
                str(edge_case)
                if edge_case
                else ""
            )
        }

        self.feedback.append(feedback_item)

        with open(
            FEEDBACK_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                self.feedback,
                file,
                indent=2
            )

        return {
            "message": "Feedback stored successfully.",
            "total_feedback": len(self.feedback)
        }

    def check_relevance(self, code, language):

        text = str(language) + " " + str(code)

        vector = self.false_positive_vectorizer.transform(
            [text]
        )

        prediction = self.false_positive_model.predict(
            vector
        )[0]

        return prediction

    def _risk_weight(self, risk):

        risk_weights = {
            "CRITICAL": 1.00,
            "HIGH": 0.90,
            "MEDIUM": 0.70,
            "LOW": 0.50
        }

        return risk_weights.get(
            str(risk).upper(),
            0.50
        )

    def recommend(
        self,
        code,
        language=None,
        top_k=3
    ):

        if not code or not str(code).strip():
            raise ValueError("Code cannot be empty.")

        if not language or not str(language).strip():
            raise ValueError("Language cannot be empty.")

        query = str(code).strip()

        # False-positive verification
        relevance = self.check_relevance(
            query,
            language
        )

        if relevance == "GENERIC_INTEGER":
            return {
                "relevant": False,
                "classification": relevance,
                "results": []
            }

        # Similarity search
        query_vector = self.vectorizer.transform(
            [query]
        )

        similarities = cosine_similarity(
            query_vector,
            self.pattern_vectors
        )[0]

        candidates = self.dataset.copy()

        candidates["similarity"] = similarities

        # Prefer same language
        language_mask = (
            candidates["Language"]
            .str.lower()
            == str(language).lower()
        )

        language_candidates = candidates[
            language_mask
        ]

        if not language_candidates.empty:
            candidates = language_candidates

        # Risk-aware ranking
        candidates["risk_weight"] = candidates[
            "Risk"
        ].apply(self._risk_weight)

        candidates["ranking_score"] = (
            candidates["similarity"] * 0.70
            +
            candidates["risk_weight"] * 0.30
        )

        candidates = candidates.sort_values(
            by="ranking_score",
            ascending=False
        )

        candidates = candidates.head(top_k)

        results = []

        for _, row in candidates.iterrows():

            result = {
                "matched_pattern": str(
                    row["Pattern"]
                ),
                "language": str(
                    row["Language"]
                ),
                "risk": str(
                    row["Risk"]
                ),
                "recommendation": str(
                    row["Recommendation"]
                ),
                "similarity": round(
                    float(row["similarity"]),
                    4
                ),
                "ranking_score": round(
                    float(row["ranking_score"]),
                    4
                )
            }

            if "Source" in row.index:
                result["source"] = str(
                    row["Source"]
                )

            if "Source URL" in row.index:
                result["source_url"] = str(
                    row["Source URL"]
                )

            results.append(result)

        return {
            "relevant": True,
            "classification": relevance,
            "feedback_records": len(self.feedback),
            "results": results
        }


advisor = RemediationAdvisorV2()