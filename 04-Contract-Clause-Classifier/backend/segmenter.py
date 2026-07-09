"""segmenter.py — Heuristic clause splitter"""
import re

MIN_WORDS = 30

def split_into_clauses(text):
    numbered = re.split(r"\n\s*(?:\d+\.\d*|(?:Article|Section|Clause)\s+\d+)\s", text)
    raw_clauses = numbered if len(numbered) > 3 else re.split(r"\n{2,}", text)
    return [
        {"index": i + 1, "text": c.strip()}
        for i, c in enumerate(raw_clauses)
        if len(c.strip().split()) >= MIN_WORDS
    ]
