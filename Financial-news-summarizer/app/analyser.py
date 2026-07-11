"""analyser.py — OpenAI sentiment analysis"""
import json, os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

SYSTEM = """You are a financial analyst. Return ONLY valid JSON:
{"summary":"3 plain-English sentences","sentiment":"Bullish"|"Bearish"|"Neutral"|"Mixed",
 "sentiment_reasoning":"one sentence","key_facts":["2-3 specific facts"],"market_impact":"short-term"|"long-term"|"unclear"}"""

def analyse_article(article):
    content = f"Ticker:{article['ticker']}\n{article['title']}\n{article['description']}"
    resp = client.chat.completions.create(
        model="gpt-4o-mini", response_format={"type":"json_object"},
        messages=[{"role":"system","content":SYSTEM},{"role":"user","content":content}],
        temperature=0.2)
    return {**article, **json.loads(resp.choices[0].message.content)}

def aggregate_ticker_sentiment(articles):
    sentiments = [a.get("sentiment") for a in articles if a.get("sentiment")]
    counts = {s:sentiments.count(s) for s in set(sentiments)}
    overall = max(counts,key=counts.get) if counts else "Neutral"
    return {"overall_sentiment":overall,"total_articles":len(articles),
            "bullish_count":counts.get("Bullish",0),"bearish_count":counts.get("Bearish",0),
            "neutral_count":counts.get("Neutral",0),"mixed_count":counts.get("Mixed",0)}
