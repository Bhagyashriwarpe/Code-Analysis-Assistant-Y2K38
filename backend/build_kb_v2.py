import os
import pandas as pd


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SOURCE_FILE = os.path.join(
    BASE_DIR,
    "Y2038_Week1_Dataset_500_Unique_With_Recommendations.xlsx"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "Y2038_Knowledge_Base_v2.xlsx"
)


REQUIRED_COLUMNS = [
    "Pattern",
    "Language",
    "Risk",
    "Recommendation"
]


def normalize_text(value):
    if pd.isna(value):
        return ""

    return str(value).strip()


def validate_row(row):

    for column in REQUIRED_COLUMNS:

        if not normalize_text(row[column]):
            return False

    return True


def build_knowledge_base():

    if not os.path.exists(SOURCE_FILE):

        raise FileNotFoundError(
            "Source dataset not found: "
            + SOURCE_FILE
        )

    df = pd.read_excel(
        SOURCE_FILE
    )

    print(
        "Original rows:",
        len(df)
    )

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:

        raise ValueError(
            "Missing columns: "
            + ", ".join(missing)
        )

    df = df.copy()

    for column in REQUIRED_COLUMNS:

        df[column] = (
            df[column]
            .map(normalize_text)
        )

    df["Validation_Status"] = (
        df.apply(
            validate_row,
            axis=1
        )
        .map(
            {
                True: "VALID",
                False: "INVALID"
            }
        )
    )

    df["Source_Type"] = (
        "Existing validated dataset"
    )

    df = df[
        df["Validation_Status"]
        == "VALID"
    ]

    df = df.drop_duplicates(
        subset=[
            "Pattern",
            "Language"
        ]
    )

    df = df.reset_index(
        drop=True
    )

    print(
        "Valid unique patterns:",
        len(df)
    )

    print(
        "\nPatterns by language:"
    )

    print(
        df["Language"]
        .value_counts()
        .to_string()
    )

    print(
        "\nRisk distribution:"
    )

    print(
        df["Risk"]
        .value_counts()
        .to_string()
    )

    df.to_excel(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nKB v2.0 created:"
    )

    print(
        OUTPUT_FILE
    )


if __name__ == "__main__":

    build_knowledge_base()