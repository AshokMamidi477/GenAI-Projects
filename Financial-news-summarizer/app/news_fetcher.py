"""news_fetcher.py — NewsAPI integration"""
import os, requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("NEWS_API_KEY")

def fetch_news(ticker, days_back=7, max_articles=5):
    params = {"q":f"{ticker} stock","from":(date.today()-timedelta(days=days_back)).isoformat(),
              "sortBy":"publishedAt","language":"en","pageSize":max_articles,"apiKey":KEY}
    resp = requests.get("https://newsapi.org/v2/everything", params=params, timeout=10)
    resp.raise_for_status()
    return [{"ticker":ticker,"url":a.get("url",""),"title":a.get("title",""),
             "description":a.get("description","") or "",
             "published_at":a.get("publishedAt",""),"source":a.get("source",{}).get("name","")}
            for a in resp.json().get("articles",[])
            if a.get("title") and "[Removed]" not in a.get("title","")]
