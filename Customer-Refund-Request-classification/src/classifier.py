"""classifier.py — Gemini classification + CSV export"""

import json
import os
from datetime import datetime

import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv
import joblib
import hybrid_classifier

print("Hybrid module loaded from:", hybrid_classifier.__file__)
print("classify_email function:", hybrid_classifier.classify_email)

load_dotenv()

# Configure Gemini
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# Load ML classifier
ml_model = joblib.load(
    "src/ML/classifier.pkl"
)

tfidf_vectorizer = joblib.load(
    "src/ML/tfidf.pkl"
)


SYSTEM_PROMPT = """
You are a customer support triage specialist.

Analyze the customer email and return ONLY valid JSON.

Format:

{
 "request_type":"Refund|Return|Exchange|Complaint|Other",
 "urgency":"critical|high|medium|low",
 "one_line_summary":"max 15 words",
 "suggested_action":"issue_refund|process_return|send_replacement|escalate_to_manager|standard_reply|flag_for_review",
 "chargeback_risk":true|false
}

Rules:

Urgency:
- critical = chargeback, legal threat, review threat
- high = not received >14 days, wrong item
- medium = normal customer request
- low = general question

Never add extra text outside JSON.
"""

def classify_batch(emails):
    results = []
    print(f"Processing {len(emails)} emails...")

    for index, email in enumerate(emails, start=1):
        print(
            f"Classifying email {index}/{len(emails)}: "
            f"{email.get('subject','')}"
        )
        try:
            classification = hybrid_classifier.classify_email(
            email.get("from",""),
            email.get("subject",""),
            email.get("body","")
        )
            results.append({
                **email,
                **classification
            })

        except Exception as e:
            print( f"Failed email {index}: {e}" )
            results.append({
                **email,
                "request_type": None,
                "urgency": None,
                "one_line_summary": f"Error: {e}",
                "suggested_action": None,
                "chargeback_risk": None
            })

    if not results:
        print("No emails classified")
        return pd.DataFrame()

    df = pd.DataFrame(results)

    # Sort urgency
    urgency_order = pd.CategoricalDtype(
        [
            "critical",
            "high",
            "medium",
            "low"
        ],
        ordered=True
    )
    
    if "urgency" in df.columns:
        df["urgency"] = df["urgency"].astype(
            urgency_order
        )
        df = df.sort_values(
            "urgency"
        )

    os.makedirs(
        "output",
        exist_ok=True
    )

    path = ("output/"
        f"classified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

    df.to_csv(
        path,
        index=False
    )

    print()
    print(f"Saved CSV: {path}")

    return df

if __name__ == "__main__":

    from gmail_client import (
        get_gmail_service,
        fetch_unread_emails
    )

    print("🔐 Connecting to Gmail...")

    service = get_gmail_service()

    print("📩 Fetching unread emails...")

    emails = fetch_unread_emails(
        service,
        label="INBOX",
        max_results=10
    )

    print(
        f"Found {len(emails)} unread emails"
    )

    if emails:
        classify_batch(emails)
    else:
        print(
            "No unread emails found"
        )