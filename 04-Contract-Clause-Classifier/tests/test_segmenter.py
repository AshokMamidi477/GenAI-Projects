"""test_segmenter.py"""
import sys; sys.path.insert(0, ".")
from backend.segmenter import split_into_clauses

def test_short_clauses_filtered():
    text = "Short.\n\n" + ("word " * 35)
    clauses = split_into_clauses(text)
    for c in clauses:
        assert len(c["text"].split()) >= 30

def test_empty_returns_empty():
    assert split_into_clauses("") == []

def test_numbered_sections_detected():
    text = """
1. DEFINITIONS
This Agreement uses the following terms as defined herein and all capitalized terms shall have the meanings set forth below in this document.

2. OBLIGATIONS
The Service Provider shall deliver all work products within the agreed timeframe as specified in Schedule A.
"""
    result = split_into_clauses(text)
    assert len(result) >= 1
