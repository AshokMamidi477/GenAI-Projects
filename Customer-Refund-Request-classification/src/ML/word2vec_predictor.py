import joblib
import numpy as np

from ML.config import (
    WORD2VEC_MODEL_PATH,
    WORD2VEC_PATH
)


model = joblib.load(
    WORD2VEC_MODEL_PATH
)

word2vec = joblib.load(
    WORD2VEC_PATH
)


def get_sentence_vector(text):

    words = text.lower().split()

    vectors = []

    for word in words:
        if word in word2vec.wv:
            vectors.append(
                word2vec.wv[word]
            )

    if not vectors:
        return np.zeros(
            word2vec.vector_size
        )

    return np.mean(
        vectors,
        axis=0
    )


def predict_request_type_word2vec(text):

    vector = get_sentence_vector(text)

    prediction = model.predict(
        [vector]
    )[0]

    probability = model.predict_proba(
        [vector]
    )[0]

    confidence = probability.max()


    return {
        "request_type": prediction,
        "confidence": confidence
    }