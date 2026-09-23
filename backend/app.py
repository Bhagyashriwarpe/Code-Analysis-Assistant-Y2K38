from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import os

from report_generator import create_report
from remediation_advisor_v2 import advisor
from remediation_engine import ContextAwareRemediationEngine
from prompt_security import sanitize_prompt
from severity_scoring import score_finding
from executive_briefing import build_briefing

from rag_knowledge_base import search_knowledge
from risk_analysis import (
    calculate_effort,
    calculate_priority,
    business_risk
)


app = Flask(__name__)
CORS(app)


# ====================================================
# LOAD EXISTING ML MODEL
# ====================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "svm_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "tfidf_vectorizer.pkl"
)

RECOMMENDATION_DATASET_PATH = os.path.join(
    BASE_DIR,
    "recommendation_dataset.pkl"
)

FALSE_POSITIVE_MODEL_PATH = os.path.join(
    BASE_DIR,
    "false_positive_model.pkl"
)

FALSE_POSITIVE_VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "false_positive_vectorizer.pkl"
)


model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)

recommendation_dataset = joblib.load(
    RECOMMENDATION_DATASET_PATH
)

false_positive_model = joblib.load(
    FALSE_POSITIVE_MODEL_PATH
)

false_positive_vectorizer = joblib.load(
    FALSE_POSITIVE_VECTORIZER_PATH
)


# ====================================================
# PREPARE RECOMMENDATION DATASET
# ====================================================

recommendation_dataset = (
    recommendation_dataset.copy()
)

recommendation_dataset["input_text"] = (
    recommendation_dataset["input_text"]
    .fillna("")
    .astype(str)
)

recommendation_vectors = (
    vectorizer.transform(
        recommendation_dataset["input_text"]
    )
)


# ====================================================
# Y2038 RULE-BASED DETECTION
# ====================================================

def detect_y2038_rule(code):

    code = str(code)

    # Safe 64-bit patterns
    safe_patterns = [

        r"\bint64_t\b",
        r"\buint64_t\b",
        r"\blong long\b",
        r"\btime64_t\b",

        r"\bstd::chrono\b",
        r"\bInstant\b",
        r"\bLong\b"
    ]

    for pattern in safe_patterns:

        if re.search(
            pattern,
            code,
            re.IGNORECASE
        ):
            return "LOW"


    # High-risk patterns
    high_risk_patterns = [

        r"\bint\s+\w*timestamp\w*",
        r"\bint32_t\s+\w*timestamp\w*",
        r"\bint\s+\w*time\w*",

        r"\btime_t\s+\w*timestamp\w*",

        r"\bSystem\.currentTimeMillis\s*\(",
        r"\bgetTime\s*\(",

        r"\bfromtimestamp\s*\(",
        r"\bdatetime\.fromtimestamp\s*\("
    ]


    for pattern in high_risk_patterns:

        if re.search(
            pattern,
            code,
            re.IGNORECASE
        ):
            return "HIGH"


    return None


# ====================================================
# FALSE-POSITIVE SUPPRESSION
# ====================================================

def check_false_positive(
    code,
    language
):

    text = (
        str(language)
        + "\n"
        + str(code)
    )

    vector = (
        false_positive_vectorizer.transform(
            [text]
        )
    )

    prediction = (
        false_positive_model.predict(
            vector
        )[0]
    )

    return prediction


# ====================================================
# RISK-ONLY ANALYZER
# ====================================================

def analyze_risk_only(
    code,
    language
):

    ml_vector = vectorizer.transform(
        [code]
    )

    ml_prediction = model.predict(
        ml_vector
    )[0]

    rule_prediction = detect_y2038_rule(
        code
    )

    initial_prediction = (
        rule_prediction
        or ml_prediction
    )

    normalized_prediction = (
        str(initial_prediction).upper()
    )

    prediction = normalized_prediction

    suppressed = False

    false_positive_check = None

    if normalized_prediction in [
        "HIGH",
        "MEDIUM"
    ]:

        false_positive_check = (
            check_false_positive(
                code,
                language
            )
        )

        if (
            false_positive_check
            == "GENERIC_INTEGER"
        ):

            prediction = "LOW"
            suppressed = True

    return prediction


# ====================================================
# REMEDIATION ENGINE
# ====================================================

remediation_engine = ContextAwareRemediationEngine(
    advisor=advisor,
    analyzer=analyze_risk_only
)


# ====================================================
# ANALYZE API
# ====================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "Request body is required."
            }), 400


        code = data.get(
            "code",
            ""
        )

        language = data.get(
            "language",
            ""
        )


        if not str(code).strip():

            return jsonify({
                "error": "Code cannot be empty."
            }), 400


        if not str(language).strip():

            return jsonify({
                "error": "Language cannot be empty."
            }), 400


        code = str(code).strip()
        language = str(language).strip()


        # ====================================================
        # EXISTING ML PREDICTION
        # ====================================================

        ml_vector = (
            vectorizer.transform(
                [code]
            )
        )

        ml_prediction = (
            model.predict(
                ml_vector
            )[0]
        )


        # ====================================================
        # RULE-BASED PREDICTION
        # ====================================================

        rule_prediction = (
            detect_y2038_rule(
                code
            )
        )


        # ====================================================
        # INITIAL PREDICTION
        # ====================================================

        if rule_prediction:

            initial_prediction = (
                rule_prediction
            )

        else:

            initial_prediction = (
                ml_prediction
            )


        # ====================================================
        # FALSE-POSITIVE CHECK
        # ====================================================

        false_positive_check = None
        suppressed = False

        prediction = (
            initial_prediction
        )

        normalized_prediction = (
            str(initial_prediction).upper()
        )

        if normalized_prediction in [
            "HIGH",
            "MEDIUM"
        ]:

            false_positive_check = (
                check_false_positive(
                    code,
                    language
                )
            )

            if (
                false_positive_check
                == "GENERIC_INTEGER"
            ):

                prediction = "LOW"
                suppressed = True


        # ====================================================
        # EXISTING RECOMMENDATION DATASET MATCH
        # ====================================================

        query_vector = (
            vectorizer.transform(
                [code]
            )
        )


        from sklearn.metrics.pairwise import (
            cosine_similarity
        )


        similarities = cosine_similarity(
            query_vector,
            recommendation_vectors
        )[0]


        best_index = (
            similarities.argmax()
        )


        matched_pattern = (
            str(
                recommendation_dataset.iloc[
                    best_index
                ]["Pattern"]
            )
        )


        matched_risk = (
            str(
                recommendation_dataset.iloc[
                    best_index
                ]["Risk"]
            )
        )


        # ====================================================
        # REMEDIATION ADVISOR V2
        # ====================================================

        remediation_result = (
            advisor.recommend(
                code,
                language,
                3
            )
        )


        if remediation_result[
            "relevant"
        ]:

            if remediation_result[
                "results"
            ]:

                recommendation = (
                    remediation_result[
                        "results"
                    ][0][
                        "recommendation"
                    ]
                )

            else:

                recommendation = None


            advisor_matches = (
                remediation_result[
                    "results"
                ]
            )

        else:

            recommendation = None

            advisor_matches = []


        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "risk":
                prediction,

            "initial_risk":
                initial_prediction,

            "ml_prediction":
                ml_prediction,

            "rule_prediction":
                rule_prediction,

            "false_positive_check":
                false_positive_check,

            "suppressed":
                suppressed,

            "recommendation":
                recommendation,

            "matched_pattern":
                matched_pattern,

            "matched_risk":
                matched_risk,

            "remediation_advisor":
                remediation_result,

            "advisor_matches":
                advisor_matches

        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# REMEDIATION API
# ====================================================

@app.route(
    "/remediate",
    methods=["POST"]
)
def remediate():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                    "Request body is required."
            }), 400


        code = str(
            data.get(
                "code",
                ""
            )
        ).strip()


        language = str(
            data.get(
                "language",
                ""
            )
        ).strip()


        if not code:

            return jsonify({
                "error":
                    "Code cannot be empty."
            }), 400


        if not language:

            return jsonify({
                "error":
                    "Language cannot be empty."
            }), 400


        return jsonify(
            remediation_engine.remediate(
                code,
                language
            )
        )


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# FEEDBACK API
# ====================================================

@app.route(
    "/feedback",
    methods=["POST"]
)
def feedback():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                    "Request body is required."
            }), 400


        required = [
            "code",
            "language",
            "accepted_recommendation"
        ]


        missing = [
            key
            for key in required
            if key not in data
        ]


        if missing:

            return jsonify({
                "error":
                    "Missing fields: "
                    + ", ".join(missing)
            }), 400


        return jsonify(
            advisor.add_feedback(
                data["code"],
                data["language"],
                data["accepted_recommendation"],
                data.get(
                    "corrected_recommendation"
                ),
                data.get(
                    "edge_case"
                )
            )
        )


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# CHAT API
# ====================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                    "Request body is required."
            }), 400


        code = str(
            data.get(
                "code",
                ""
            )
        ).strip()


        language = str(
            data.get(
                "language",
                ""
            )
        ).strip()


        question = sanitize_prompt(
            data.get(
                "question",
                "Analyze and remediate this code."
            )
        )


        if not code or not language:

            return jsonify({
                "error":
                    "Both code and language are required."
            }), 400


        result = (
            remediation_engine.remediate(
                code,
                language
            )
        )


        result["question"] = question


        return jsonify(
            result
        )


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# SANITIZE API
# ====================================================

@app.route(
    "/sanitize",
    methods=["POST"]
)
def sanitize():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                    "Request body is required."
            }), 400


        return jsonify({

            "sanitized":
                sanitize_prompt(
                    data.get(
                        "text",
                        ""
                    )
                )

        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# PROMPT LIBRARY API
# ====================================================

@app.route(
    "/prompts",
    methods=["GET"]
)
def prompts():

    import json

    prompt_file = os.path.join(
        BASE_DIR,
        "prompt_library.json"
    )


    if not os.path.exists(
        prompt_file
    ):

        return jsonify({
            "error":
                "Prompt library has not been generated."
        }), 404


    with open(
        prompt_file,
        "r",
        encoding="utf-8"
    ) as file:

        return jsonify(
            json.load(file)
        )


# ====================================================
# ENTERPRISE SEVERITY API
# ====================================================

@app.route(
    "/severity-score",
    methods=["POST"]
)
def severity_score():

    try:

        data = request.get_json() or {}


        result = score_finding(

            data.get(
                "severity",
                "LOW"
            ),

            data.get(
                "reachability",
                1
            ),

            data.get(
                "production_exposure",
                1
            ),

            data.get(
                "persistence",
                1
            ),

            data.get(
                "external_dependency",
                1
            )
        )


        return jsonify(
            result
        )


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# ====================================================
# EXECUTIVE BRIEFING API
# ====================================================

@app.route(
    "/executive-briefing",
    methods=["POST"]
)
def executive_briefing():

    try:

        data = request.get_json() or {}


        return jsonify(
            build_briefing(
                data.get(
                    "findings",
                    []
                )
            )
        )


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# ====================================================
# BUSINESS ANALYSIS API
# ====================================================

@app.route(
    "/business-analysis",
    methods=["POST"]
)
def business_analysis():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                    "Request body is required."
            }), 400


        risk = data.get(
            "risk",
            "LOW"
        )


        code = data.get(
            "code",
            ""
        )


        language = data.get(
            "language",
            ""
        )


        effort = calculate_effort(
            risk
        )


        import json

        profile_path = os.path.join(
            BASE_DIR,
            "risk_profiles.json"
        )


        with open(
            profile_path,
            "r",
            encoding="utf-8"
        ) as profile_file:

            risk_profiles = json.load(
                profile_file
            )


        scores = risk_profiles.get(
            str(risk).upper(),
            risk_profiles["LOW"]
        )


        priority = calculate_priority(
            *scores
        )


        business = business_risk(
            risk
        )


        return jsonify({

            "risk":
                risk,

            "effort":
                effort,

            "priority":
                priority,

            "business_risk":
                business

        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# GENERATE REPORT API
# ====================================================

@app.route(
    "/generate-report",
    methods=["POST"]
)
def generate_report():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                    "Request body is required."
            }), 400


        code = data.get(
            "code",
            ""
        )


        language = data.get(
            "language",
            "C"
        )


        if not code:

            return jsonify({
                "error":
                    "Code is required"
            }), 400


        # ====================================================
        # USE EXISTING ANALYZE PIPELINE
        # ====================================================

        with app.test_client() as client:

            response = client.post(
                "/analyze",
                json={
                    "code": code,
                    "language": language
                }
            )


            if response.status_code != 200:

                return jsonify({

                    "error":
                        "Analysis failed",

                    "details":
                        response.get_json()

                }), response.status_code


            analysis = (
                response.get_json()
            )


        # ====================================================
        # PREPARE REPORT FINDING
        # ====================================================

        finding = {

            "code":
                code,

            "language":
                language,

            "risk":
                analysis.get(
                    "risk",
                    "LOW"
                ),

            "recommendation":
                analysis.get(
                    "recommendation",
                    ""
                ),

            "matched_pattern":
                analysis.get(
                    "matched_pattern",
                    ""
                ),

            "suppressed":
                analysis.get(
                    "suppressed",
                    False
                )

        }


        # ====================================================
        # GENERATE REPORT
        # ====================================================

        report_path = create_report(
            [finding]
        )


        return jsonify({

            "message":
                "Report generated successfully",

            "report":
                report_path

        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ====================================================
# HOME
# ====================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify({

        "message":
            "CodeGuard AI Backend Running 🚀",

        "status":
            "success",

        "version":
            "Remediation Advisor v2.0"

    })


# ====================================================
# RUN SERVER
# ====================================================

if __name__ == "__main__":

    app.run(
        debug=False,
        port=5000
    )