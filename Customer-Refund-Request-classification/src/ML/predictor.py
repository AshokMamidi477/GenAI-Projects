import joblib

from ML.config import (
    TFIDF_MODEL_PATH,
    TFIDF_VECTORIZER_PATH
)


model = joblib.load(
    TFIDF_MODEL_PATH
)

tfidf = joblib.load(
    TFIDF_VECTORIZER_PATH
)


def predict_request_type(text):

    X = tfidf.transform(
        [text]
    )

    prediction = model.predict(
        X
    )[0]

    probabilities = model.predict_proba(
        X
    )[0]

    confidence = probabilities.max()


    return {
        "request_type": prediction,
        "confidence": float(confidence)
    }