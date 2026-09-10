from flask import Flask, request, jsonify
from flask_cors import CORS

import joblib
import re


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

CORS(app)


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load("svm_model.pkl")


# ============================================================
# LOAD TF-IDF VECTORIZER
# ============================================================

vectorizer = joblib.load("tfidf_vectorizer.pkl")


# ============================================================
# LOAD RECOMMENDATION DATASET
# ============================================================

recommendation_dataset = joblib.load(
    "recommendation_dataset.pkl"
)


# ============================================================
# Y2038 RULE-BASED CHECK
# ============================================================

def detect_y2038_rule(code):

    code_lower = code.lower()


    # --------------------------------------------------------
    # SAFE 64-BIT TIMESTAMP PATTERNS
    # --------------------------------------------------------

    safe_patterns = [

        r"\bint64_t\b",

        r"\buint64_t\b",

        r"\bint64\b",

        r"\buint64\b",

        r"\blong\s+long\b",

        r"\btime64_t\b"

    ]


    for pattern in safe_patterns:

        if re.search(
            pattern,
            code_lower
        ):

            return "LOW"


    # --------------------------------------------------------
    # HIGH-RISK 32-BIT TIMESTAMP PATTERNS
    # --------------------------------------------------------

    high_risk_patterns = [

        r"\bint\s+timestamp\s*=",

        r"\bint32_t\s+timestamp",

        r"\bint32\s+timestamp",

        r"\bint\s+time_stamp\s*=",

        r"\bint32_t\s+time_stamp",

        r"\bint\s+ts\s*="

    ]


    for pattern in high_risk_patterns:

        if re.search(
            pattern,
            code_lower
        ):

            return "HIGH"


    # --------------------------------------------------------
    # time(NULL) STORED IN INTEGER
    # --------------------------------------------------------

    if re.search(
        r"\bint\s+\w+\s*=\s*time\s*\(\s*null\s*\)",
        code_lower
    ):

        return "HIGH"


    # --------------------------------------------------------
    # int32 CAST
    # --------------------------------------------------------

    if re.search(
        r"\(\s*int32_t\s*\)\s*time\s*\(",
        code_lower
    ):

        return "HIGH"


    # --------------------------------------------------------
    # NO CLEAR RULE
    # --------------------------------------------------------

    return None


# ============================================================
# ANALYZE API
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze_code():

    try:

        # ----------------------------------------------------
        # GET JSON DATA
        # ----------------------------------------------------

        data = request.get_json()


        if not data:

            return jsonify({

                "error":
                "No data received."

            }), 400


        # ----------------------------------------------------
        # GET CODE
        # ----------------------------------------------------

        code = data.get(
            "code",
            ""
        )


        # ----------------------------------------------------
        # VALIDATE CODE
        # ----------------------------------------------------

        if not code.strip():

            return jsonify({

                "error":
                "Code cannot be empty."

            }), 400


        # ====================================================
        # ML PREDICTION
        # ====================================================

        # IMPORTANT:
        # Model is trained using code/pattern only.

        input_text = code


        code_vector = vectorizer.transform(

            [input_text]

        )


        ml_prediction = model.predict(

            code_vector

        )[0]


        # ====================================================
        # RULE-BASED Y2038 CHECK
        # ====================================================

        rule_prediction = detect_y2038_rule(

            code

        )


        # ====================================================
        # FINAL RISK
        # ====================================================

        if rule_prediction is not None:

            prediction = rule_prediction

        else:

            prediction = ml_prediction


        # ====================================================
        # FIND SIMILAR DATASET PATTERN
        # ====================================================

        dataset_text = (

            recommendation_dataset[
                "input_text"
            ]
            .fillna("")
            .astype(str)
            .tolist()

        )


        dataset_vectors = vectorizer.transform(

            dataset_text

        )


        # ====================================================
        # FIND BEST MATCH
        # ====================================================

        similarity_scores = (

            dataset_vectors
            @ code_vector.T

        ).toarray().flatten()


        best_index = int(

            similarity_scores.argmax()

        )


        # ====================================================
        # GET MATCHED ROW
        # ====================================================

        matched_row = (

            recommendation_dataset
            .iloc[best_index]

        )


        # ====================================================
        # DATASET VALUES
        # ====================================================

        matched_pattern = str(

            matched_row[
                "Pattern"
            ]

        )


        # ====================================================
        # USE FINAL RISK FOR DISPLAYED PATTERN RISK
        # ====================================================

        matched_risk = str(

            prediction

        )


        # ====================================================
        # RECOMMENDATION
        # ====================================================

        recommendation = str(

            matched_row[
                "Recommendation"
            ]

        )


        # ====================================================
        # SAFE CODE RECOMMENDATION
        # ====================================================

        if prediction == "LOW":

            recommendation = (

                "No change required; keep "
                "the existing 64-bit timestamp "
                "representation."

            )


        # ====================================================
        # HIGH RISK RECOMMENDATION
        # ====================================================

        elif prediction == "HIGH":

            recommendation = (

                "Replace 32-bit timestamp "
                "storage with int64_t or another "
                "verified 64-bit representation."

            )


        # ====================================================
        # MEDIUM RISK RECOMMENDATION
        # ====================================================

        elif prediction == "MEDIUM":

            recommendation = (

                "Review the timestamp representation "
                "and ensure that time values are stored "
                "using a verified 64-bit representation."

            )


        # ====================================================
        # RESPONSE
        # ====================================================

        response = {

            "risk":
                str(prediction),

            "recommendation":
                recommendation,

            "matched_pattern":
                matched_pattern,

            "matched_risk":
                matched_risk

        }


        # ====================================================
        # TERMINAL OUTPUT
        # ====================================================

        print(
            "\n================================"
        )

        print(
            "CODE ANALYSIS"
        )

        print(
            "================================"
        )

        print(
            "ML Prediction:",
            ml_prediction
        )

        print(
            "Rule Prediction:",
            rule_prediction
        )

        print(
            "Final Risk:",
            prediction
        )

        print(
            "Matched Pattern:",
            matched_pattern
        )

        print(
            "Pattern Risk:",
            matched_risk
        )

        print(
            "Recommendation:",
            recommendation
        )

        print(
            "================================\n"
        )


        # ====================================================
        # SEND RESPONSE
        # ====================================================

        return jsonify(

            response

        )


    except Exception as e:

        print(
            "\n================================"
        )

        print(
            "ERROR"
        )

        print(
            "================================"
        )

        print(
            str(e)
        )

        print(
            "================================\n"
        )


        return jsonify({

            "error":
            str(e)

        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000

    )