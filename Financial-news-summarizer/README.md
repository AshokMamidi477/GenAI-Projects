# Project 8 — Financial News Summarizer with Sentiment

![Level](https://img.shields.io/badge/Level-Beginner-green)
![Industry](https://img.shields.io/badge/Industry-Finance-orange)
![Stack](https://img.shields.io/badge/Stack-Google%20Gemini%20%7C%20NewsAPI%20%7C%20Streamlit-blue)

## Business Problem

Retail investors follow dozens of tickers and must process hundreds of financial articles daily.

Traditional sentiment analysis tools often fail to understand financial context. For example:

> "Company missed earnings estimates but raised future guidance"

is not simply positive or negative.

Affordable AI-powered financial intelligence is difficult for individual investors to access.

This project demonstrates how Generative AI can analyze financial news, summarize key information, and provide sentiment insights using Google's Gemini LLM.

---

## Project Objective

A Streamlit dashboard that:

- Accepts stock tickers from users
- Fetches recent financial news using NewsAPI
- Uses Google Gemini AI to:
  - Summarize articles
  - Classify sentiment:
    - Bullish
    - Bearish
    - Neutral
    - Mixed
  - Extract important financial facts
  - Analyze possible market impact
- Aggregates sentiment by ticker
- Displays an interactive financial intelligence dashboard

---

## System Architecture

```mermaid
graph TD
    A[User enters stock tickers] --> B[Streamlit Dashboard]
    B --> C[NewsAPI Financial Articles]
    C --> D[Google Gemini AI Analysis]
    D --> E[Structured JSON Response]
    E --> F[Ticker Sentiment Aggregation]
    F --> G[Financial News Dashboard]
AI Model Used
Google Gemini

This project uses Google's Gemini Generative AI model instead of OpenAI.

Gemini is responsible for:

Financial article summarization
Sentiment classification
Key fact extraction
Market impact reasoning

Advantages:

Strong reasoning capabilities
JSON structured responses
Cost-effective API usage
Easy integration with Python applications
Folder Structure
project-8-financial-news-summarizer/

├── app/
│   ├── app.py
│   ├── news_fetcher.py
│   └── analyser.py
│
├── tests/
│   └── test_analyser.py
│
├── samples/
│   └── cached_results.json
│
├── .env.example
├── requirements.txt
└── README.md
Setup
pip install -r requirements.txt

cp .env.example .env

streamlit run app/app.py
Step-by-Step Implementation Guide

This guide walks through building the complete project.

Step 1: Project Setup
1.1 Create Project Folder and Virtual Environment
mkdir project-08-financial-news-summarizer

cd project-08-financial-news-summarizer

python -m venv venv

Activate environment:

Mac/Linux
source venv/bin/activate
Windows
venv\Scripts\activate

A virtual environment keeps project dependencies isolated.

1.2 Create Folder Structure
mkdir app tests samples

touch app/app.py
touch app/news_fetcher.py
touch app/analyser.py

touch tests/test_analyser.py

touch requirements.txt
touch .env.example
touch .env
1.3 Install Dependencies

Add the following packages:

google-generativeai>=0.8.0
requests>=2.31.0
streamlit>=1.35.0
pandas>=2.0.0
python-dotenv>=1.0.0
pytest>=8.0.0

Install:

pip install -r requirements.txt
1.4 Configure Environment Variables

Create .env.example

GEMINI_API_KEY=your_google_gemini_api_key
NEWS_API_KEY=your_newsapi_key

Copy:

cp .env.example .env
API Keys Setup
Google Gemini API Key
Go to Google AI Studio:

https://aistudio.google.com/

Sign in with Google account
Create API Key
Copy the key into .env

Example:

GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxx
News API Key
Go to:

https://newsapi.org

Create a free account
Generate API key

Add:

NEWS_API_KEY=xxxxxxxxxxxxxxxx
1.5 Protect Secrets

Create .gitignore

.env
credentials.json
token.json
__pycache__/
venv/

Never commit API keys to GitHub.

Step 2: Understand Folder Structure
project-8-financial-news-summarizer/

├── app/
│
│   ├── app.py
│       Streamlit dashboard
│
│   ├── news_fetcher.py
│       Fetches financial articles from NewsAPI
│
│   └── analyser.py
│       Sends articles to Gemini AI
│       Returns summary + sentiment
│
├── samples/
│   └── cached_results.json
│       Demo data without API calls
│
├── tests/
│   └── test_analyser.py
│
├── requirements.txt
│
├── .env
│
└── README.md

The complete data flow:

User Input
    |
    ↓
Stock Ticker
    |
    ↓
NewsAPI
    |
    ↓
Financial Articles
    |
    ↓
Google Gemini AI
    |
    ↓
Summary + Sentiment + Facts
    |
    ↓
Streamlit Dashboard
Step 3: Build News Fetcher (app/news_fetcher.py)

Continuing with Part 2 — Gemini AI Analyzer + Streamlit Dashboard.

Copy this after Part 1 in your README.md.

# Step 3: Build the News Fetcher (`app/news_fetcher.py`)

This module connects to NewsAPI and retrieves recent financial news articles for a stock ticker.

```python
"""news_fetcher.py — NewsAPI integration"""

import os
import requests
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
Fetch Financial Articles
def fetch_news(ticker, days_back=7, max_articles=5):

    params = {
        "q": f"{ticker} stock",
        "from": (date.today() - timedelta(days=days_back)).isoformat(),
        "sortBy": "publishedAt",
        "language": "en",
        "pageSize": max_articles,
        "apiKey": NEWS_API_KEY
    }


    response = requests.get(
        "https://newsapi.org/v2/everything",
        params=params,
        timeout=10
    )


    response.raise_for_status()


    articles = []

    for article in response.json().get("articles", []):

        title = article.get("title", "")

        if not title or "[Removed]" in title:
            continue


        articles.append({

            "ticker": ticker,

            "title": title,

            "description":
                article.get("description", "") or "",

            "source":
                article.get("source", {}).get("name", ""),

            "url":
                article.get("url", ""),

            "published_at":
                article.get("publishedAt", "")
        })


    return articles
Why NewsAPI?

NewsAPI provides:

Recent financial articles
Article metadata
Source information
Published timestamps

The project uses NewsAPI only for data collection.

Google Gemini performs the actual AI reasoning.

Step 4: Build Gemini AI Analyzer (app/analyser.py)

This module sends financial articles to Google's Gemini model.

Gemini performs:

Article summarization
Sentiment classification
Key fact extraction
Market impact analysis
Import Gemini SDK
"""analyser.py — Google Gemini financial analysis"""

import os
import json

import google.generativeai as genai

from dotenv import load_dotenv


load_dotenv()


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-2.0-flash"
)
Gemini System Prompt

The prompt defines the expected AI response format.

SYSTEM_PROMPT = """

You are a professional financial analyst.

Analyze the financial news article.

Return ONLY valid JSON:

{
"summary":
"3 simple sentences",

"sentiment":
"Bullish | Bearish | Neutral | Mixed",

"sentiment_reasoning":
"Explain why",

"key_facts":
[
"fact 1",
"fact 2",
"fact 3"
],

"market_impact":
"short-term | long-term | unclear"
}


Rules:

Bullish:
Positive business growth,
strong earnings,
positive guidance.

Bearish:
Negative earnings,
lawsuits,
weak guidance,
major risks.

Neutral:
Informational news without clear impact.

Mixed:
Positive and negative signals together.

"""
Analyze Article Using Gemini
def analyse_article(article):

    content = f"""

Ticker:
{article['ticker']}


Headline:
{article['title']}


Description:

{article['description']}

"""


    response = model.generate_content(

        SYSTEM_PROMPT + content

    )


    result = response.text


    # Remove markdown formatting if Gemini returns ```json
    result = result.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    )


    analysis = json.loads(result)


    return {
        **article,
        **analysis
    }
Why Gemini JSON Output?

Without structured output:

Example responses may vary:

Positive
Very bullish
Looks good
Strong buy signal

This creates inconsistent data.

JSON forces predictable fields:

{
"sentiment":"Bullish",
"market_impact":"short-term"
}

which can directly power the dashboard.

Aggregate Sentiment Per Stock
def aggregate_ticker_sentiment(articles):

    sentiments = [

        article.get("sentiment")

        for article in articles

        if article.get("sentiment")

    ]


    counts = {

        sentiment:
        sentiments.count(sentiment)

        for sentiment in set(sentiments)

    }


    overall = (

        max(
            counts,
            key=counts.get
        )

        if counts

        else "Neutral"

    )


    return {

        "overall_sentiment":
            overall,

        "total_articles":
            len(articles),

        "bullish_count":
            counts.get("Bullish",0),

        "bearish_count":
            counts.get("Bearish",0),

        "neutral_count":
            counts.get("Neutral",0),

        "mixed_count":
            counts.get("Mixed",0)

    }
Step 5: Build Streamlit Dashboard (app/app.py)
"""app.py — Financial news dashboard"""


import json
import os
import time

import streamlit as st

from news_fetcher import fetch_news

from analyser import (
    analyse_article,
    aggregate_ticker_sentiment
)


st.set_page_config(

    page_title=
    "Financial News Summarizer",

    page_icon="📈",

    layout="wide"

)


st.title(
    "📈 Financial News Summarizer with Gemini AI"
)
Sentiment Icons
ICONS = {

    "Bullish":"🟢",

    "Bearish":"🔴",

    "Neutral":"⚪",

    "Mixed":"🟡"

}
User Controls
with st.sidebar:


    tickers_input = st.text_input(

        "Stock Symbols",

        value="AAPL,TSLA,NVDA"

    )


    days_back = st.slider(

        "Days of News",

        1,

        30,

        7

    )


    max_articles = st.slider(

        "Articles Per Stock",

        1,

        5,

        3

    )


    analyze_button = st.button(

        "Analyze News"

    )


    demo_button = st.button(

        "Load Demo"

    )
Demo Mode
if demo_button:

    path = os.path.join(

        os.path.dirname(__file__),

        "../samples/cached_results.json"

    )


    if os.path.exists(path):

        with open(path) as file:

            st.session_state["results"] = json.load(file)


        st.success(
            "Demo data loaded"
        )
# Run Gemini Financial Analysis

When the user clicks **Analyze News**, the application:

1. Reads stock tickers
2. Fetches financial news
3. Sends articles to Gemini AI
4. Receives structured JSON analysis
5. Displays sentiment and summaries


```python
if analyze_button:

    tickers = [

        ticker.strip().upper()

        for ticker in tickers_input.split(",")

        if ticker.strip()

    ]


    results = {}


    progress = st.progress(0)


    for index, ticker in enumerate(tickers):

        try:

            articles = fetch_news(

                ticker,

                days_back,

                max_articles

            )


            analyzed_articles = []


            for article in articles:

                try:

                    result = analyse_article(article)

                    analyzed_articles.append(result)


                    # Prevent API rate limits

                    time.sleep(0.5)


                except Exception as error:

                    st.warning(

                        f"Gemini error: {error}"

                    )


            results[ticker] = {

                "articles":
                    analyzed_articles,

                **aggregate_ticker_sentiment(

                    analyzed_articles

                )

            }


        except Exception as error:

            st.error(

                f"{ticker}: {error}"

            )


        progress.progress(

            (index + 1) / len(tickers)

        )


    st.session_state["results"] = results
Display Financial Dashboard
if "results" in st.session_state:


    results = st.session_state["results"]


    st.subheader(
        "Market Sentiment Overview"
    )


    columns = st.columns(

        max(len(results),1)

    )


    for column, (ticker,data) in zip(

        columns,

        results.items()

    ):


        column.metric(

            ticker,

            ICONS.get(

                data["overall_sentiment"],

                "⚪"

            )
            +

            " "

            +

            data["overall_sentiment"]

        )


    st.divider()



    for ticker,data in results.items():


        st.header(ticker)


        st.write(

            f"""

            Total Articles:

            {data['total_articles']}

            """

        )


        for article in data["articles"]:


            sentiment = article.get(

                "sentiment",

                "Neutral"

            )


            with st.expander(

                ICONS.get(sentiment,"⚪")

                +

                " "

                +

                article["title"]

            ):


                st.caption(

                    article.get(

                        "source",

                        ""

                    )

                )


                st.write(

                    "**Summary**"

                )


                st.write(

                    article.get(

                        "summary",

                        ""

                    )

                )


                st.write(

                    "**Reasoning**"

                )


                st.write(

                    article.get(

                        "sentiment_reasoning",

                        ""

                    )

                )


                st.write(

                    "**Key Facts**"

                )


                for fact in article.get(

                    "key_facts",

                    []

                ):

                    st.markdown(

                        f"- {fact}"

                    )
Step 6: Running the Application
Activate Virtual Environment

Mac/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate
Start Streamlit

From project root:

streamlit run app/app.py

The browser will open:

http://localhost:8501
Demo Mode (No API Cost)

The project includes cached demo data.

Use:

Sidebar → Load Demo

This allows testing:

Dashboard UI
Sentiment badges
Article summaries
Key facts

without using:

Gemini API credits
NewsAPI requests
Step 7: Testing

Run automated tests:

pytest tests/test_analyser.py -v

Example test:

def test_sentiment_values():

    allowed = [

        "Bullish",

        "Bearish",

        "Neutral",

        "Mixed"

    ]

    assert "Bullish" in allowed
Step 8: Troubleshooting
Error	Cause	Fix
google.auth.exceptions.DefaultCredentialsError	Gemini API key missing	Check GEMINI_API_KEY inside .env
API key not valid	Incorrect Gemini key	Generate a new key from Google AI Studio
requests.exceptions.HTTPError: 401	Invalid NewsAPI key	Verify NEWS_API_KEY
ModuleNotFoundError	Running from wrong folder	Run streamlit run app/app.py from project root
Gemini returns markdown JSON	Model wrapped JSON with ```	Code removes markdown formatting before parsing
JSONDecodeError	Gemini response format changed	Improve prompt or add JSON validation
Rate limit errors	Too many Gemini requests	Increase time.sleep() delay
Empty ticker results	No recent articles	Increase date range
Security Best Practices

Never commit:

.env

or API credentials.

Your .gitignore should contain:

.env
__pycache__/
venv/

Example:

git status

Before committing verify:

.env

is NOT listed.

Project Skills Demonstrated
Generative AI
Google Gemini API integration
Prompt engineering
Structured JSON output
LLM-based sentiment analysis
Financial reasoning
Python
API integration
Environment variables
JSON processing
Exception handling
Data aggregation
Data Engineering
External API ingestion
Data transformation
Caching
Dashboard visualization
Streamlit
Interactive dashboard
User inputs
Metrics
Expandable article views
Future Enhancements
AI Features
Add Gemini-powered financial Q&A chatbot
Compare multiple companies using AI
Generate weekly investment reports
Add earnings-call transcript analysis
Data Features
Historical sentiment charts
Portfolio sentiment scoring
Sector-level sentiment analysis
Stock correlation analysis
Deployment
Deploy Streamlit application
Add scheduled daily reports
Send email summaries
Add cloud deployment using Google Cloud Run
Time Estimate
Mode	Duration
Self-paced	10–13 hours
Instructor-guided	5–7 hours
Final Architecture Summary
             User
              |
              |
        Streamlit App
              |
              |
        Stock Tickers
              |
              |
          NewsAPI
              |
              |
     Financial Articles
              |
              |
        Google Gemini
              |
              |
 Summary + Sentiment + Facts
              |
              |
      Financial Dashboard
Project Outcome

This project demonstrates a complete Generative AI application:

✅ Real-world financial data ingestion
✅ Google Gemini LLM integration
✅ Prompt engineering
✅ Structured AI responses
✅ Sentiment intelligence
✅ Interactive Streamlit dashboard

The application transforms raw financial news into actionable investor insights using Generative AI.