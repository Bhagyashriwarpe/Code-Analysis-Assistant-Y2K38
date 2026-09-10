import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. LOAD DATASET
# ============================================================

DATASET_FILE = (
    "Y2038_Week1_Dataset_500_Unique_With_Recommendations.xlsx"
)


df = pd.read_excel(

    DATASET_FILE

)


print(
    "================================"
)

print(
    "Dataset loaded successfully!"
)

print(
    "================================"
)

print(
    "Dataset size:",
    len(df)
)


print(
    "\nColumns:"
)

print(
    df.columns.tolist()
)


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

df.columns = (

    df.columns
    .str.strip()

)


# ============================================================
# 3. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [

    "Pattern",

    "Language",

    "Risk",

    "Recommendation"

]


for column in required_columns:

    if column not in df.columns:

        raise ValueError(

            f"Required column '{column}' "
            "not found in dataset."

        )


# ============================================================
# 4. CLEAN DATA
# ============================================================

df["Pattern"] = (

    df["Pattern"]
    .fillna("")
    .astype(str)

)


df["Language"] = (

    df["Language"]
    .fillna("")
    .astype(str)

)


df["Risk"] = (

    df["Risk"]
    .fillna("")
    .astype(str)
    .str.strip()

)


df["Recommendation"] = (

    df["Recommendation"]
    .fillna("")
    .astype(str)

)


# ============================================================
# 5. CREATE INPUT TEXT
# ============================================================

# IMPORTANT:
#
# Language is NOT used here.
#
# The model learns directly from the code pattern.

df["input_text"] = (

    df["Pattern"]

)


# ============================================================
# 6. REMOVE EMPTY DATA
# ============================================================

df = df[

    (df["input_text"].str.strip() != "") &

    (df["Risk"].str.strip() != "")

].copy()


# ============================================================
# 7. DISPLAY RISK DISTRIBUTION
# ============================================================

print(
    "\n================================"
)

print(
    "Risk Distribution"
)

print(
    "================================"
)

print(

    df["Risk"].value_counts()

)


# ============================================================
# 8. FEATURES AND TARGET
# ============================================================

X = df["input_text"]

y = df["Risk"]


# ============================================================
# 9. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = (

    train_test_split(

        X,

        y,

        test_size=0.20,

        random_state=42,

        stratify=y

    )

)


# ============================================================
# 10. TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(

    lowercase=True,

    analyzer="word",

    ngram_range=(1, 3),

    min_df=1,

    sublinear_tf=True

)


# ============================================================
# 11. TRANSFORM DATA
# ============================================================

X_train_vectorized = (

    vectorizer.fit_transform(

        X_train

    )

)


X_test_vectorized = (

    vectorizer.transform(

        X_test

    )

)


print(
    "\n================================"
)

print(
    "TF-IDF Feature Extraction"
)

print(
    "================================"
)

print(

    "Training shape:",

    X_train_vectorized.shape

)

print(

    "Testing shape:",

    X_test_vectorized.shape

)


# ============================================================
# 12. TRAIN LINEAR SVM
# ============================================================

model = LinearSVC(

    C=1.5,

    class_weight="balanced",

    random_state=42

)


model.fit(

    X_train_vectorized,

    y_train

)


# ============================================================
# 13. PREDICTION
# ============================================================

predictions = (

    model.predict(

        X_test_vectorized

    )

)


# ============================================================
# 14. ACCURACY
# ============================================================

accuracy = (

    accuracy_score(

        y_test,

        predictions

    )

)


print(
    "\n================================"
)

print(
    "MODEL EVALUATION"
)

print(
    "================================"
)

print(

    "Accuracy:",

    round(

        accuracy * 100,

        2

    ),

    "%"

)


# ============================================================
# 15. CLASSIFICATION REPORT
# ============================================================

print(
    "\nClassification Report:"
)


print(

    classification_report(

        y_test,

        predictions,

        zero_division=0

    )

)


# ============================================================
# 16. SAVE MODEL
# ============================================================

joblib.dump(

    model,

    "svm_model.pkl"

)


# ============================================================
# 17. SAVE VECTORIZER
# ============================================================

joblib.dump(

    vectorizer,

    "tfidf_vectorizer.pkl"

)


# ============================================================
# 18. SAVE RECOMMENDATION DATASET
# ============================================================

recommendation_dataset = df[

    [

        "Pattern",

        "Language",

        "Risk",

        "Recommendation",

        "input_text"

    ]

].copy()


joblib.dump(

    recommendation_dataset,

    "recommendation_dataset.pkl"

)


# ============================================================
# 19. FINAL OUTPUT
# ============================================================

print(
    "\n================================"
)

print(
    "MODEL TRAINING COMPLETED!"
)

print(
    "================================"
)


print(

    "Dataset size:",

    len(df)

)


print(

    "Classes:",

    sorted(

        df["Risk"].unique()

    )

)


print(
    "\nFiles created:"
)


print(
    "1. svm_model.pkl"
)

print(
    "2. tfidf_vectorizer.pkl"
)

print(
    "3. recommendation_dataset.pkl"
)


print(
    "\n================================"
)

print(
    "READY FOR FLASK"
)

print(
    "================================"
)