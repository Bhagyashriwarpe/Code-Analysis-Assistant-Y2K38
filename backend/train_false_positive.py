import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


# ============================================================
# 1. Generic integer examples
# ============================================================

generic_examples = [

    # ---------------- C ----------------
    ("int count = 10;", "C"),
    ("int id = 101;", "C"),
    ("int index = 0;", "C"),
    ("int size = 50;", "C"),
    ("int quantity = 100;", "C"),
    ("int retryCount = 3;", "C"),
    ("int userId = 1001;", "C"),
    ("int itemCount = 25;", "C"),
    ("int numberOfUsers = 500;", "C"),
    ("int statusCode = 200;", "C"),
    ("int port = 8080;", "C"),
    ("int age = 25;", "C"),
    ("int score = 90;", "C"),
    ("int marks = 85;", "C"),
    ("int length = 20;", "C"),
    ("int width = 10;", "C"),
    ("int height = 15;", "C"),
    ("int price = 500;", "C"),
    ("int amount = 1000;", "C"),
    ("int position = 5;", "C"),
    ("int row = 3;", "C"),
    ("int column = 4;", "C"),
    ("int page = 2;", "C"),
    ("int level = 5;", "C"),
    ("int priority = 1;", "C"),
    ("int attempts = 3;", "C"),
    ("int result = 0;", "C"),
    ("int flag = 1;", "C"),
    ("int x = 10;", "C"),
    ("int value = 50;", "C"),
    ("int data = 100;", "C"),
    ("int n = 20;", "C"),
    ("int a = 5;", "C"),
    ("int b = 10;", "C"),
    ("int code = 404;", "C"),
    ("int errorCode = 500;", "C"),
    ("int socket = 4;", "C"),
    ("int fd = 3;", "C"),
    ("int capacity = 100;", "C"),
    ("int offset = 10;", "C"),
    ("int counter = 0;", "C"),

    # ---------------- C++ ----------------
    ("int count = 10;", "C++"),
    ("int id = 101;", "C++"),
    ("int index = 0;", "C++"),
    ("int size = 50;", "C++"),
    ("int quantity = 100;", "C++"),
    ("int retryCount = 3;", "C++"),
    ("int userId = 1001;", "C++"),
    ("int itemCount = 25;", "C++"),
    ("int numberOfUsers = 500;", "C++"),
    ("int statusCode = 200;", "C++"),
    ("int port = 8080;", "C++"),
    ("int age = 25;", "C++"),
    ("int score = 90;", "C++"),
    ("int marks = 85;", "C++"),
    ("int length = 20;", "C++"),
    ("int width = 10;", "C++"),
    ("int height = 15;", "C++"),
    ("int price = 500;", "C++"),
    ("int amount = 1000;", "C++"),
    ("int position = 5;", "C++"),
    ("int row = 3;", "C++"),
    ("int column = 4;", "C++"),
    ("int page = 2;", "C++"),
    ("int level = 5;", "C++"),
    ("int priority = 1;", "C++"),
    ("int attempts = 3;", "C++"),
    ("int result = 0;", "C++"),
    ("int flag = 1;", "C++"),
    ("int x = 10;", "C++"),
    ("int value = 50;", "C++"),
    ("int data = 100;", "C++"),
    ("int n = 20;", "C++"),
    ("int a = 5;", "C++"),
    ("int b = 10;", "C++"),
    ("int code = 404;", "C++"),
    ("int errorCode = 500;", "C++"),
    ("int capacity = 100;", "C++"),
    ("int offset = 10;", "C++"),
    ("int counter = 0;", "C++"),

    # ---------------- Java ----------------
    ("int count = 10;", "Java"),
    ("int id = 101;", "Java"),
    ("int index = 0;", "Java"),
    ("int size = 50;", "Java"),
    ("int quantity = 100;", "Java"),
    ("int retryCount = 3;", "Java"),
    ("int userId = 1001;", "Java"),
    ("int itemCount = 25;", "Java"),
    ("int numberOfUsers = 500;", "Java"),
    ("int statusCode = 200;", "Java"),
    ("int port = 8080;", "Java"),
    ("int age = 25;", "Java"),
    ("int score = 90;", "Java"),
    ("int marks = 85;", "Java"),
    ("int length = 20;", "Java"),
    ("int width = 10;", "Java"),
    ("int height = 15;", "Java"),
    ("int price = 500;", "Java"),
    ("int amount = 1000;", "Java"),
    ("int position = 5;", "Java"),
    ("int row = 3;", "Java"),
    ("int column = 4;", "Java"),
    ("int page = 2;", "Java"),
    ("int level = 5;", "Java"),
    ("int priority = 1;", "Java"),
    ("int attempts = 3;", "Java"),
    ("int result = 0;", "Java"),
    ("int flag = 1;", "Java"),
    ("int x = 10;", "Java"),
    ("int value = 50;", "Java"),
    ("int data = 100;", "Java"),
    ("int n = 20;", "Java"),
    ("int a = 5;", "Java"),
    ("int b = 10;", "Java"),
    ("int code = 404;", "Java"),
    ("int errorCode = 500;", "Java"),
    ("int capacity = 100;", "Java"),
    ("int offset = 10;", "Java"),
    ("int counter = 0;", "Java"),
]


# ============================================================
# 2. Timestamp / Y2038 examples
# ============================================================

timestamp_examples = [

    # ---------------- C ----------------

    ("int timestamp = time(NULL);", "C"),
    ("int t = time(NULL);", "C"),
    ("int ts = time(NULL);", "C"),
    ("int value = time(NULL);", "C"),
    ("int data = time(NULL);", "C"),
    ("int x = time(NULL);", "C"),
    ("int created = time(NULL);", "C"),
    ("int expiry = time(NULL);", "C"),
    ("int loginTime = time(NULL);", "C"),
    ("int startTime = time(NULL);", "C"),
    ("int endTime = time(NULL);", "C"),
    ("int currentTime = time(NULL);", "C"),
    ("int unixTime = time(NULL);", "C"),
    ("int now = time(NULL);", "C"),
    ("int32_t timestamp = time(NULL);", "C"),
    ("int32_t ts = time(NULL);", "C"),
    ("int32_t t = time(NULL);", "C"),
    ("int32_t value = time(NULL);", "C"),
    ("int created = (int)time(NULL);", "C"),
    ("int timestamp = (int)time(NULL);", "C"),
    ("int t = (int)time(NULL);", "C"),
    ("int expiry = time(NULL) + 3600;", "C"),
    ("int deadline = time(NULL) + 86400;", "C"),
    ("int start = time(NULL);", "C"),
    ("int end = time(NULL);", "C"),
    ("int seconds = time(NULL);", "C"),
    ("int epoch = time(NULL);", "C"),
    ("int login = time(NULL);", "C"),
    ("int logout = time(NULL);", "C"),
    ("int event = time(NULL);", "C"),
    ("int stamp = time(NULL);", "C"),
    ("int t1 = time(NULL);", "C"),
    ("int t2 = time(NULL);", "C"),
    ("int64_t timestamp = (int32_t)time(NULL);", "C"),
    ("int32_t expiry = (int32_t)time(NULL);", "C"),
    ("int32_t created = (int32_t)time(NULL);", "C"),
    ("int timestamp = (int)clock_gettime(CLOCK_REALTIME, NULL);", "C"),
    ("int t = gettimeofday(NULL, NULL);", "C"),
    ("int32_t seconds = (int32_t)time(NULL);", "C"),

    # ---------------- C++ ----------------

    ("int timestamp = time(NULL);", "C++"),
    ("int t = time(NULL);", "C++"),
    ("int ts = time(NULL);", "C++"),
    ("int value = time(NULL);", "C++"),
    ("int data = time(NULL);", "C++"),
    ("int x = time(NULL);", "C++"),
    ("int created = time(NULL);", "C++"),
    ("int expiry = time(NULL);", "C++"),
    ("int loginTime = time(NULL);", "C++"),
    ("int startTime = time(NULL);", "C++"),
    ("int endTime = time(NULL);", "C++"),
    ("int currentTime = time(NULL);", "C++"),
    ("int unixTime = time(NULL);", "C++"),
    ("int now = time(NULL);", "C++"),
    ("int32_t timestamp = time(NULL);", "C++"),
    ("int32_t ts = time(NULL);", "C++"),
    ("int32_t t = time(NULL);", "C++"),
    ("int created = (int)time(NULL);", "C++"),
    ("int timestamp = (int)time(NULL);", "C++"),
    ("int t = (int)time(NULL);", "C++"),
    ("int expiry = time(NULL) + 3600;", "C++"),
    ("int deadline = time(NULL) + 86400;", "C++"),
    ("int start = time(NULL);", "C++"),
    ("int end = time(NULL);", "C++"),
    ("int seconds = time(NULL);", "C++"),
    ("int epoch = time(NULL);", "C++"),
    ("int login = time(NULL);", "C++"),
    ("int logout = time(NULL);", "C++"),
    ("int event = time(NULL);", "C++"),
    ("int stamp = time(NULL);", "C++"),
    ("int t1 = time(NULL);", "C++"),
    ("int t2 = time(NULL);", "C++"),
    ("int32_t expiry = (int32_t)time(NULL);", "C++"),
    ("int32_t created = (int32_t)time(NULL);", "C++"),
    ("int seconds = static_cast<int>(time(NULL));", "C++"),
    ("int timestamp = static_cast<int>(time(NULL));", "C++"),
    ("int t = static_cast<int>(time(NULL));", "C++"),

    # ---------------- Java ----------------

    ("int timestamp = (int) System.currentTimeMillis();", "Java"),
    ("int t = (int) System.currentTimeMillis();", "Java"),
    ("int ts = (int) System.currentTimeMillis();", "Java"),
    ("int value = (int) System.currentTimeMillis();", "Java"),
    ("int data = (int) System.currentTimeMillis();", "Java"),
    ("int created = (int) System.currentTimeMillis();", "Java"),
    ("int expiry = (int) System.currentTimeMillis();", "Java"),
    ("int loginTime = (int) System.currentTimeMillis();", "Java"),
    ("int startTime = (int) System.currentTimeMillis();", "Java"),
    ("int endTime = (int) System.currentTimeMillis();", "Java"),
    ("int currentTime = (int) System.currentTimeMillis();", "Java"),
    ("int unixTime = (int) System.currentTimeMillis();", "Java"),
    ("int now = (int) System.currentTimeMillis();", "Java"),
    ("int epoch = (int) System.currentTimeMillis();", "Java"),
    ("int stamp = (int) System.currentTimeMillis();", "Java"),
    ("int seconds = (int) System.currentTimeMillis();", "Java"),
    ("int timestamp = (int) Instant.now().getEpochSecond();", "Java"),
    ("int t = (int) Instant.now().getEpochSecond();", "Java"),
    ("int ts = (int) Instant.now().getEpochSecond();", "Java"),
    ("int value = (int) Instant.now().getEpochSecond();", "Java"),
    ("int created = (int) Instant.now().getEpochSecond();", "Java"),
    ("int expiry = (int) Instant.now().getEpochSecond();", "Java"),
    ("int timestamp = (int) System.currentTimeMillis() / 1000;", "Java"),
    ("int t = (int) System.currentTimeMillis() / 1000;", "Java"),
    ("int expiry = (int) System.currentTimeMillis() + 3600;", "Java"),
    ("int deadline = (int) System.currentTimeMillis() + 86400;", "Java"),
    ("int login = (int) System.currentTimeMillis();", "Java"),
    ("int logout = (int) System.currentTimeMillis();", "Java"),
    ("int event = (int) System.currentTimeMillis();", "Java"),
    ("int start = (int) System.currentTimeMillis();", "Java"),
    ("int end = (int) System.currentTimeMillis();", "Java"),
]


# ============================================================
# 3. Create dataframe
# ============================================================

data = []

for code, language in generic_examples:
    data.append({
        "code": code,
        "language": language,
        "label": "GENERIC_INTEGER"
    })

for code, language in timestamp_examples:
    data.append({
        "code": code,
        "language": language,
        "label": "TIMESTAMP"
    })


df = pd.DataFrame(data)

df["text"] = (
    df["language"] + " " +
    df["code"]
)


# ============================================================
# 4. Display dataset information
# ============================================================

print("\nDataset size:")
print(len(df))

print("\nClass distribution:")
print(df["label"].value_counts())


# ============================================================
# 5. Train / Test split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)


# ============================================================
# 6. TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    ngram_range=(1, 3),
    lowercase=True,
    sublinear_tf=True
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# ============================================================
# 7. Train classifier
# ============================================================

model = LinearSVC(
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_tfidf, y_train)


# ============================================================
# 8. Evaluate
# ============================================================

predictions = model.predict(X_test_tfidf)

print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions
))

print("\nConfusion Matrix:")
print(confusion_matrix(
    y_test,
    predictions
))


# ============================================================
# 9. Calculate False Positive Rate
# ============================================================

# False positive:
# GENERIC_INTEGER incorrectly predicted as TIMESTAMP

safe_mask = y_test == "GENERIC_INTEGER"

false_positives = (
    (predictions == "TIMESTAMP") &
    safe_mask
).sum()

total_safe = safe_mask.sum()

if total_safe > 0:
    false_positive_rate = (
        false_positives / total_safe
    ) * 100
else:
    false_positive_rate = 0


print("\nFalse Positive Evaluation:")
print("False positives:", false_positives)
print("Safe examples:", total_safe)
print(
    f"False Positive Rate: {false_positive_rate:.2f}%"
)


# ============================================================
# 10. Save model
# ============================================================

joblib.dump(
    model,
    "false_positive_model.pkl"
)

joblib.dump(
    vectorizer,
    "false_positive_vectorizer.pkl"
)

print("\nModel saved successfully.")

print("false_positive_model.pkl")
print("false_positive_vectorizer.pkl")