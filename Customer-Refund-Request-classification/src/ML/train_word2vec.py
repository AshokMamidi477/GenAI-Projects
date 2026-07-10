import os
import joblib
import pandas as pd
import numpy as np

from gensim.models import Word2Vec

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from config import (
    DATASET_PATH,
    WORD2VEC_MODEL_PATH,
    WORD2VEC_PATH
)


# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv(DATASET_PATH)

print(
    f"Dataset Loaded: {len(df)} rows"
)


# ==========================================
# Prepare Text
# ==========================================

sentences = [
    text.lower().split()
    for text in df["text"]
]


labels = df["request_type"]


# ==========================================
# Train Word2Vec
# ==========================================

word2vec = Word2Vec(
    sentences,
    vector_size=100,
    window=5,
    min_count=1,
    workers=4,
    epochs=100
)


print("Word2Vec training completed")


# ==========================================
# Convert Email to Vector
# ==========================================

def email_to_vector(email):

    words = email.lower().split()

    vectors = []

    for word in words:

        if word in word2vec.wv:
            vectors.append(
                word2vec.wv[word]
            )

    if len(vectors) == 0:
        return np.zeros(100)

    return np.mean(
        vectors,
        axis=0
    )


X = np.array(
    [
        email_to_vector(text)
        for text in df["text"]
    ]
)


y = labels


# ==========================================
# Train/Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# Train Classifier
# ==========================================

classifier = LogisticRegression(
    max_iter=1000
)


classifier.fit(
    X_train,
    y_train
)


# ==========================================
# Evaluate
# ==========================================

prediction = classifier.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    prediction
)


print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


print(
    classification_report(
        y_test,
        prediction
    )
)


# ==========================================
# Save Models
# ==========================================

joblib.dump(
    classifier,
    WORD2VEC_MODEL_PATH
)

joblib.dump(
    word2vec,
    WORD2VEC_PATH
)


print("Models saved")
print(WORD2VEC_MODEL_PATH)
print(WORD2VEC_PATH)


# ==========================================
# Test Example
# ==========================================

sample = [
    "My order arrived broken and damaged"
]


sample_vector = np.array(
    [
        email_to_vector(sample[0])
    ]
)


result = classifier.predict(
    sample_vector
)


probability = classifier.predict_proba(
    sample_vector
)


print("-" * 50)
print(
    "Sample:",
    sample[0]
)

print(
    "Prediction:",
    result[0]
)

print(
    "Confidence:",
    probability.max()
)