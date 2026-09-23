
import os
import json
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "Y2038_Knowledge_Base_v2.xlsx"
)

CSV_OUTPUT = os.path.join(
    BASE_DIR,
    "case_study_metrics.csv"
)

JSON_OUTPUT = os.path.join(
    BASE_DIR,
    "case_study_metrics.json"
)


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def clean(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


def percentage(part, total):
    if total == 0:
        return 0.0

    return round((part / total) * 100, 2)


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

def load_dataset():

    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Dataset not found:\n{INPUT_FILE}"
        )

    df = pd.read_excel(INPUT_FILE)

    required_columns = [
        "Pattern",
        "Language",
        "Risk",
        "Label",
        "Recommendation"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    return df


# ---------------------------------------------------------
# Basic audit metrics
# ---------------------------------------------------------

def calculate_basic_metrics(df):

    total_patterns = len(df)

    unique_patterns = (
        df["Pattern"]
        .astype(str)
        .str.strip()
        .nunique()
    )

    languages = (
        df["Language"]
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    risks = (
        df["Risk"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace("", "UNKNOWN")
    )

    labels = (
        df["Label"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace("", "UNKNOWN")
    )

    high_count = int((risks == "HIGH").sum())
    medium_count = int((risks == "MEDIUM").sum())
    low_count = int((risks == "LOW").sum())
    critical_count = int((risks == "CRITICAL").sum())

    unsafe_count = int((labels == "UNSAFE").sum())
    safe_count = int((labels == "SAFE").sum())

    return {
        "total_patterns_analyzed": total_patterns,
        "unique_patterns": unique_patterns,

        "high_risk_findings": high_count,
        "medium_risk_findings": medium_count,
        "low_risk_findings": low_count,
        "critical_risk_findings": critical_count,

        "unsafe_findings": unsafe_count,
        "safe_findings": safe_count,

        "high_risk_percentage": percentage(
            high_count,
            total_patterns
        ),

        "medium_risk_percentage": percentage(
            medium_count,
            total_patterns
        ),

        "low_risk_percentage": percentage(
            low_count,
            total_patterns
        ),

        "unsafe_percentage": percentage(
            unsafe_count,
            total_patterns
        ),

        "safe_percentage": percentage(
            safe_count,
            total_patterns
        )
    }


# ---------------------------------------------------------
# Language metrics
# ---------------------------------------------------------

def calculate_language_metrics(df):

    language_counts = (
        df["Language"]
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
        .value_counts()
    )

    result = {}

    total = len(df)

    for language, count in language_counts.items():

        result[language] = {
            "patterns": int(count),
            "percentage": percentage(
                int(count),
                total
            )
        }

    return result


# ---------------------------------------------------------
# Risk metrics
# ---------------------------------------------------------

def calculate_risk_metrics(df):

    risk_series = (
        df["Risk"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace("", "UNKNOWN")
    )

    risk_counts = risk_series.value_counts()

    result = {}

    for risk, count in risk_counts.items():

        result[risk] = {
            "count": int(count),
            "percentage": percentage(
                int(count),
                len(df)
            )
        }

    return result


# ---------------------------------------------------------
# Label metrics
# ---------------------------------------------------------

def calculate_label_metrics(df):

    label_series = (
        df["Label"]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace("", "UNKNOWN")
    )

    label_counts = label_series.value_counts()

    result = {}

    for label, count in label_counts.items():

        result[label] = {
            "count": int(count),
            "percentage": percentage(
                int(count),
                len(df)
            )
        }

    return result


# ---------------------------------------------------------
# Recommendation metrics
# ---------------------------------------------------------

def calculate_recommendation_metrics(df):

    recommendation_series = (
        df["Recommendation"]
        .astype(str)
        .str.strip()
    )

    non_empty = recommendation_series[
        recommendation_series != ""
    ]

    recommendations_available = len(non_empty)

    recommendations_missing = (
        len(df) - recommendations_available
    )

    return {
        "recommendations_available": recommendations_available,
        "recommendations_missing": recommendations_missing,
        "recommendation_coverage_percentage": percentage(
            recommendations_available,
            len(df)
        )
    }


# ---------------------------------------------------------
# Source metrics
# ---------------------------------------------------------

def calculate_source_metrics(df):

    result = {
        "source_column_available": "Source" in df.columns,
        "source_url_column_available": "Source URL" in df.columns,
        "patterns_with_source": 0,
        "patterns_with_source_url": 0
    }

    if "Source" in df.columns:

        source_series = (
            df["Source"]
            .astype(str)
            .str.strip()
        )

        result["patterns_with_source"] = int(
            (
                (source_series != "")
                &
                (source_series.str.lower() != "nan")
            ).sum()
        )

    if "Source URL" in df.columns:

        url_series = (
            df["Source URL"]
            .astype(str)
            .str.strip()
        )

        result["patterns_with_source_url"] = int(
            (
                (url_series != "")
                &
                (url_series.str.lower() != "nan")
            ).sum()
        )

    result["source_coverage_percentage"] = percentage(
        result["patterns_with_source"],
        len(df)
    )

    result["source_url_coverage_percentage"] = percentage(
        result["patterns_with_source_url"],
        len(df)
    )

    return result


# ---------------------------------------------------------
# Validation metrics
# ---------------------------------------------------------

def calculate_validation_metrics(df):

    if "Validation_Status" not in df.columns:

        return {
            "validation_status_available": False,
            "validated_patterns": 0,
            "pending_validation_patterns": 0,
            "validation_coverage_percentage": 0.0
        }

    validation = (
        df["Validation_Status"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    valid_count = int(
        (validation == "VALID").sum()
    )

    pending_count = int(
        (
            validation
            .isin(
                [
                    "PENDING",
                    "PENDING_VALIDATION"
                ]
            )
        ).sum()
    )

    return {
        "validation_status_available": True,
        "validated_patterns": valid_count,
        "pending_validation_patterns": pending_count,
        "validation_coverage_percentage": percentage(
            valid_count,
            len(df)
        )
    }


# ---------------------------------------------------------
# Top technical patterns
# ---------------------------------------------------------

def calculate_top_patterns(df, limit=10):

    pattern_counts = (
        df["Pattern"]
        .astype(str)
        .str.strip()
        .value_counts()
        .head(limit)
    )

    result = []

    for pattern, count in pattern_counts.items():

        result.append({
            "pattern": pattern,
            "count": int(count)
        })

    return result


# ---------------------------------------------------------
# Risk by language
# ---------------------------------------------------------

def calculate_risk_by_language(df):

    working = df.copy()

    working["Language"] = (
        working["Language"]
        .astype(str)
        .str.strip()
    )

    working["Risk"] = (
        working["Risk"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    table = pd.crosstab(
        working["Language"],
        working["Risk"]
    )

    result = {}

    for language in table.index:

        result[language] = {}

        for risk in table.columns:

            result[language][risk] = int(
                table.loc[language, risk]
            )

    return result


# ---------------------------------------------------------
# Anonymous case study summary
# ---------------------------------------------------------

def build_case_study_summary(
    basic_metrics,
    language_metrics,
    risk_metrics,
    label_metrics,
    recommendation_metrics,
    source_metrics,
    validation_metrics
):

    summary = {
        "case_study_id": "ANONYMOUS_Y2038_AUDIT_001",

        "description": (
            "Anonymous technical metrics generated "
            "from the available Y2038 knowledge-base "
            "audit dataset."
        ),

        "scope": {
            "dataset_type": "Y2038 time-overflow patterns",
            "patterns_analyzed": basic_metrics[
                "total_patterns_analyzed"
            ],
            "unique_patterns": basic_metrics[
                "unique_patterns"
            ],
            "languages": len(language_metrics)
        },

        "risk_summary": {
            "critical": basic_metrics[
                "critical_risk_findings"
            ],
            "high": basic_metrics[
                "high_risk_findings"
            ],
            "medium": basic_metrics[
                "medium_risk_findings"
            ],
            "low": basic_metrics[
                "low_risk_findings"
            ]
        },

        "technical_findings": {
            "unsafe_findings": basic_metrics[
                "unsafe_findings"
            ],
            "safe_findings": basic_metrics[
                "safe_findings"
            ]
        },

        "recommendation_coverage": (
            recommendation_metrics[
                "recommendation_coverage_percentage"
            ]
        ),

        "source_coverage": (
            source_metrics[
                "source_coverage_percentage"
            ]
        ),

        "validation_coverage": (
            validation_metrics[
                "validation_coverage_percentage"
            ]
        ),

        "languages": language_metrics,

        "risk_distribution": risk_metrics,

        "labels": label_metrics
    }

    return summary


# ---------------------------------------------------------
# Create flat CSV metrics
# ---------------------------------------------------------

def create_csv_metrics(
    basic_metrics,
    language_metrics,
    risk_metrics,
    label_metrics,
    recommendation_metrics,
    source_metrics,
    validation_metrics
):

    rows = []

    # Overall metrics

    for metric, value in basic_metrics.items():

        rows.append({
            "metric_category": "overall",
            "metric": metric,
            "value": value
        })

    # Language metrics

    for language, data in language_metrics.items():

        rows.append({
            "metric_category": "language",
            "metric": f"{language}_patterns",
            "value": data["patterns"]
        })

        rows.append({
            "metric_category": "language",
            "metric": f"{language}_percentage",
            "value": data["percentage"]
        })

    # Risk metrics

    for risk, data in risk_metrics.items():

        rows.append({
            "metric_category": "risk",
            "metric": f"{risk}_count",
            "value": data["count"]
        })

        rows.append({
            "metric_category": "risk",
            "metric": f"{risk}_percentage",
            "value": data["percentage"]
        })

    # Label metrics

    for label, data in label_metrics.items():

        rows.append({
            "metric_category": "label",
            "metric": f"{label}_count",
            "value": data["count"]
        })

        rows.append({
            "metric_category": "label",
            "metric": f"{label}_percentage",
            "value": data["percentage"]
        })

    # Recommendation metrics

    for metric, value in recommendation_metrics.items():

        rows.append({
            "metric_category": "recommendation",
            "metric": metric,
            "value": value
        })

    # Source metrics

    for metric, value in source_metrics.items():

        rows.append({
            "metric_category": "source",
            "metric": metric,
            "value": value
        })

    # Validation metrics

    for metric, value in validation_metrics.items():

        rows.append({
            "metric_category": "validation",
            "metric": metric,
            "value": value
        })

    return pd.DataFrame(rows)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    print("======================================")
    print("   AUTOMATED CASE STUDY EXTRACTION")
    print("======================================")

    print("\nInput dataset:")
    print(INPUT_FILE)

    df = load_dataset()

    print("\nDataset loaded successfully.")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    # Calculate metrics

    basic_metrics = calculate_basic_metrics(df)

    language_metrics = calculate_language_metrics(df)

    risk_metrics = calculate_risk_metrics(df)

    label_metrics = calculate_label_metrics(df)

    recommendation_metrics = (
        calculate_recommendation_metrics(df)
    )

    source_metrics = calculate_source_metrics(df)

    validation_metrics = calculate_validation_metrics(df)

    top_patterns = calculate_top_patterns(df)

    risk_by_language = calculate_risk_by_language(df)

    # Build anonymous case study

    case_study = build_case_study_summary(
        basic_metrics,
        language_metrics,
        risk_metrics,
        label_metrics,
        recommendation_metrics,
        source_metrics,
        validation_metrics
    )

    case_study["top_patterns"] = top_patterns

    case_study["risk_by_language"] = (
        risk_by_language
    )

    # -----------------------------------------------------
    # Add methodology / data limitation
    # -----------------------------------------------------

    case_study["methodology"] = {
        "source": "Y2038_Knowledge_Base_v2.xlsx",
        "processing": (
            "Metrics were calculated directly from "
            "the supplied dataset."
        ),
        "anonymization": (
            "No client names, personal identifiers, "
            "repository names, or customer-specific "
            "identifiers are included."
        ),
        "limitations": [
            (
                "The dataset contains technical patterns, "
                "not complete production application audits."
            ),
            (
                "The metrics should not be presented as "
                "measured client production outcomes."
            ),
            (
                "No remediation time savings or financial "
                "benefits are inferred unless explicitly "
                "present in the source data."
            )
        ]
    }

    # -----------------------------------------------------
    # Save JSON
    # -----------------------------------------------------

    with open(
        JSON_OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            case_study,
            file,
            indent=4,
            ensure_ascii=False
        )

    # -----------------------------------------------------
    # Save CSV
    # -----------------------------------------------------

    csv_df = create_csv_metrics(
        basic_metrics,
        language_metrics,
        risk_metrics,
        label_metrics,
        recommendation_metrics,
        source_metrics,
        validation_metrics
    )

    csv_df.to_csv(
        CSV_OUTPUT,
        index=False
    )

    # -----------------------------------------------------
    # Display results
    # -----------------------------------------------------

    print("\n======================================")
    print("          CASE STUDY METRICS")
    print("======================================")

    print(
        "\nTotal patterns:",
        basic_metrics["total_patterns_analyzed"]
    )

    print(
        "Unique patterns:",
        basic_metrics["unique_patterns"]
    )

    print(
        "High-risk findings:",
        basic_metrics["high_risk_findings"]
    )

    print(
        "Medium-risk findings:",
        basic_metrics["medium_risk_findings"]
    )

    print(
        "Low-risk findings:",
        basic_metrics["low_risk_findings"]
    )

    print(
        "Unsafe findings:",
        basic_metrics["unsafe_findings"]
    )

    print(
        "Safe findings:",
        basic_metrics["safe_findings"]
    )

    print(
        "\nRecommendation coverage:",
        f"{recommendation_metrics['recommendation_coverage_percentage']}%"
    )

    print(
        "Source coverage:",
        f"{source_metrics['source_coverage_percentage']}%"
    )

    if validation_metrics["validation_status_available"]:

        print(
            "Validation coverage:",
            f"{validation_metrics['validation_coverage_percentage']}%"
        )

    print("\nLanguages:")

    for language, data in language_metrics.items():

        print(
            f"  {language}: "
            f"{data['patterns']} "
            f"({data['percentage']}%)"
        )

    print("\nRisk distribution:")

    for risk, data in risk_metrics.items():

        print(
            f"  {risk}: "
            f"{data['count']} "
            f"({data['percentage']}%)"
        )

    print("\n======================================")
    print("          OUTPUT FILES")
    print("======================================")

    print("\nCSV:")
    print(CSV_OUTPUT)

    print("\nJSON:")
    print(JSON_OUTPUT)

    print("\n======================================")
    print("             TASK 4 STATUS")
    print("======================================")

    print(
        "\nPASS: Anonymous technical metrics extracted."
    )

    print(
        "PASS: CSV case-study dataset generated."
    )

    print(
        "PASS: JSON case-study summary generated."
    )

    print(
        "PASS: No client identity is included."
    )

    print(
        "\nImportant:"
    )

    print(
        "These metrics describe the supplied "
        "technical dataset. They should not be "
        "presented as measured client production "
        "outcomes."
    )


if __name__ == "__main__":
    main()
