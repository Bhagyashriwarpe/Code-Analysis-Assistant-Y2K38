import joblib


model = joblib.load("false_positive_model.pkl")
vectorizer = joblib.load("false_positive_vectorizer.pkl")


test_cases = [

    # ==========================================
    # Generic integers - should be SAFE
    # ==========================================

    ("C", "int count = 25;"),
    ("C", "int id = 10001;"),
    ("C", "int index = 5;"),
    ("C", "int value = 200;"),
    ("C", "int x = 50;"),
    ("C", "int retryCount = 3;"),
    ("C++", "int size = 100;"),
    ("C++", "int port = 8080;"),
    ("C++", "int statusCode = 404;"),
    ("Java", "int count = 10;"),
    ("Java", "int userId = 1001;"),
    ("Java", "int pageNumber = 5;"),
    ("Java", "int score = 90;"),

    # ==========================================
    # Timestamp risks - should be TIMESTAMP
    # ==========================================

    ("C", "int timestamp = time(NULL);"),
    ("C", "int t = time(NULL);"),
    ("C", "int value = time(NULL);"),
    ("C", "int32_t ts = time(NULL);"),
    ("C", "int expiry = time(NULL) + 3600;"),
    ("C++", "int timestamp = time(NULL);"),
    ("C++", "int t = time(NULL);"),
    ("C++", "int created = (int)time(NULL);"),
    ("C++", "int32_t ts = time(NULL);"),
    ("Java", "int timestamp = (int) System.currentTimeMillis();"),
    ("Java", "int t = (int) System.currentTimeMillis();"),
    ("Java", "int value = (int) System.currentTimeMillis();"),
    ("Java", "int ts = (int) Instant.now().getEpochSecond();"),
]


print("\nFalse-Positive Classifier Test")
print("=" * 50)


for language, code in test_cases:

    text = language + " " + code

    vector = vectorizer.transform([text])

    prediction = model.predict(vector)[0]

    print("\nLanguage :", language)
    print("Code     :", code)
    print("Prediction:", prediction)