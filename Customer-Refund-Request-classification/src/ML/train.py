import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


# ==========================================
# Paths
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(
    BASE_DIR,
    "customer_support_emails.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "classifier.pkl"
)

TFIDF_PATH = os.path.join(
    BASE_DIR,
    "tfidf.pkl"
)


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv(DATASET_PATH)

print(f"Dataset Loaded. Total rows: {len(df)}")

print(df["request_type"].value_counts())

print("-" * 50)


# ==========================================
# 2. Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["request_type"],
    test_size=0.2,
    random_state=42,
    stratify=df["request_type"]
)


# ==========================================
# 3. TF-IDF Vectorization
# ==========================================

tfidf = TfidfVectorizer(
    stop_words="english",
    sublinear_tf=True
)


X_train_tfidf = tfidf.fit_transform(
    X_train
)

X_test_tfidf = tfidf.transform(
    X_test
)


# ==========================================
# 4. Train ML Model
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)


model.fit(
    X_train_tfidf,
    y_train
)


# ==========================================
# 5. Evaluate Model
# ==========================================

y_pred = model.predict(
    X_test_tfidf
)


accuracy = accuracy_score(
    y_test,
    y_pred
)


print(
    f"Model Accuracy: {accuracy * 100:.2f}%"
)

print()

print(
    "Classification Report:"
)

print(
    classification_report(
        y_test,
        y_pred
    )
)


print("-" * 50)


# ==========================================
# 6. Save Model + TF-IDF
# ==========================================

joblib.dump(
    model,
    MODEL_PATH
)


joblib.dump(
    tfidf,
    TFIDF_PATH
)


print(
    "Model saved successfully:"
)

print(
    MODEL_PATH
)

print(
    TFIDF_PATH
)


print("-" * 50)


# ==========================================
# 7. Test Sample Email
# ==========================================

new_email = [
    "Hey, my package arrived but the box was crushed and the item inside is cracked. I'm furious."
]


new_email_tfidf = tfidf.transform(
    new_email
)


prediction = model.predict(
    new_email_tfidf
)


probabilities = model.predict_proba(
    new_email_tfidf
)


confidence = probabilities.max()


print(
    f"Sample Text: '{new_email[0]}'"
)

print(
    f"Predicted Category: {prediction[0]}"
)

print(
    f"Confidence: {confidence:.2f}"
)