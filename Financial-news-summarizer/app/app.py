"""app.py — Streamlit dashboard"""
import json, os, time
import streamlit as st
from dotenv import load_dotenv
from news_fetcher import fetch_news
from analyser import analyse_article, aggregate_ticker_sentiment

load_dotenv()
ICONS = {"Bullish":"🟢","Bearish":"🔴","Neutral":"⚪","Mixed":"🟡"}

st.set_page_config(page_title="Financial News Summarizer", page_icon="📈", layout="wide")
st.title("📈 Financial News Summarizer with Sentiment")

with st.sidebar:
    tickers_input = st.text_input("Tickers (comma-separated)", value="AAPL, TSLA, NVDA")
    days_back = st.slider("Days of news", 1, 30, 7)
    max_articles = st.slider("Articles per ticker", 1, 5, 3)
    run_btn = st.button("Analyse", type="primary")
    demo_btn = st.button("Load Demo Data")

if demo_btn:
    path = os.path.join(os.path.dirname(__file__),"../samples/cached_results.json")
    if os.path.exists(path):
        with open(path) as f: st.session_state["results"] = json.load(f)
        st.success("Demo data loaded!")

if run_btn:
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    all_results = {}
    bar = st.progress(0)
    for i, ticker in enumerate(tickers):
        try:
            articles = fetch_news(ticker, days_back, max_articles)
        except Exception as e:
            st.warning(f"{ticker}: {e}"); continue
        analysed = []
        print(f"Analysing {len(articles)} articles for {ticker}...")
        print(f"articles are  { articles } articles for {ticker}...")
        for art in articles:
            try: analysed.append(analyse_article(art)); time.sleep(0.2)
            except: pass
        all_results[ticker] = {"articles":analysed, **aggregate_ticker_sentiment(analysed)}
        bar.progress((i+1)/len(tickers))
    st.session_state["results"] = all_results

if "results" in st.session_state:
    results = st.session_state["results"]
    cols = st.columns(max(len(results),1))
    for col,(ticker,data) in zip(cols,results.items()):
        col.metric(ticker, f"{ICONS.get(data['overall_sentiment'],'⚪')} {data['overall_sentiment']}")
    st.markdown("---")
    for ticker, data in results.items():
        st.subheader(f"{ticker}")
        for art in data.get("articles",[]):
            with st.expander(f"{ICONS.get(art.get('sentiment',''),'⚪')} {art['title']}"):
                st.caption(f"{art['source']} · {art['published_at'][:10]}")
                st.markdown(f"**Summary:** {art.get('summary','')}")
                st.markdown(f"**Sentiment:** {art.get('sentiment','')} — {art.get('sentiment_reasoning','')}")
                for fact in art.get("key_facts",[]): st.markdown(f"- {fact}")
