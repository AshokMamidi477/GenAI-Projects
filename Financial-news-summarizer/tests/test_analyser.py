"""test_analyser.py"""
import sys; sys.path.insert(0,"app")
from analyser import aggregate_ticker_sentiment

def test_bullish_majority():
    a = [{"sentiment":"Bullish"},{"sentiment":"Bullish"},{"sentiment":"Bearish"}]
    assert aggregate_ticker_sentiment(a)["overall_sentiment"] == "Bullish"

def test_empty(): assert aggregate_ticker_sentiment([])["overall_sentiment"] == "Neutral"

def test_counts():
    a = [{"sentiment":"Neutral"},{"sentiment":"Neutral"},{"sentiment":"Bearish"}]
    r = aggregate_ticker_sentiment(a)
    assert r["neutral_count"]==2 and r["bearish_count"]==1
