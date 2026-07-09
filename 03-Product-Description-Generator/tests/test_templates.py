"""test_templates.py"""
import sys; sys.path.insert(0, "app")
from prompt_templates import build_prompt, parse_response

def test_prompt_contains_title():
    p = build_prompt("Test Mug", "Home", "Ceramic", "Coffee lovers", "", "Professional")
    assert "Test Mug" in p

def test_all_tones_build():
    for tone in ["Professional", "Playful", "Urgency"]:
        p = build_prompt("Widget", "Electronics", "Fast", "Techies", "widget", tone)
        assert tone in p

def test_parse_splits_correctly():
    raw = "DESCRIPTION:\nGreat product.\n\nMETA:\nGreat product. Buy now."
    desc, meta = parse_response(raw)
    assert "Great product." in desc
    assert "Buy now" in meta

def test_meta_truncated_at_155():
    raw = "DESCRIPTION:\nGood.\n\nMETA:\n" + "x" * 200
    _, meta = parse_response(raw)
    assert len(meta) <= 155
