import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DATASET_PATH = os.path.join(
    BASE_DIR,
    "customer_support_emails.csv"
)


# TF-IDF model
TFIDF_MODEL_PATH = os.path.join(
    BASE_DIR,
    "classifier.pkl"
)

TFIDF_VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "tfidf.pkl"
)


# Word2Vec model
WORD2VEC_MODEL_PATH = os.path.join(
    BASE_DIR,
    "word2vec_classifier.pkl"
)

WORD2VEC_PATH = os.path.join(
    BASE_DIR,
    "word2vec.pkl"
)