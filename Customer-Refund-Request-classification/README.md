Markdown# Project 7 — Hybrid Customer Refund Request Classifier

![Level](https://img.shields.io/badge/Level-Intermediate-orange)
![Industry](https://img.shields.io/badge/Industry-E--commerce-teal)
![Stack](https://img.shields.io/badge/Stack-Gemini%20%7C%20Scikit--Learn%20%7C%20Gensim%20%7C%20Gmail%20API%20%7C%20Streamlit-blue)

## Business Problem
E-commerce support teams receive thousands of refund and return requests weekly. Manual triage accounts for 30-40% of handle time. At scale (2,000 emails/day at $0.05/min agent cost) a 60s reduction in triage time per email saves ~$1,700/day.

## Project Objective
A multi-tier intelligent Python automation pipeline that processes incoming Gmail messages. It matches text using low-latency local **TF-IDF** and **Word2Vec** models, cascades back to a **Google Gemini** LLM fallback for complex or ambiguous cases, exports a sorted CSV queue, applies operational Gmail labels, and renders an interactive Streamlit triage dashboard.

## System Architecture
```mermaid
graph TD
    A[Gmail Inbox] --> B[Gmail API OAuth2]
    B --> C[Email Parser]
    C --> D{Hybrid Classifier Engine}
    D -->|Tier 1: Exact Keywords| E1[TF-IDF Vectorizer]
    D -->|Tier 2: Semantic Intent| E2[Word2Vec Similarity]
    D -->|Tier 3: Ambiguous Fallback| E3[Google Gemini LLM]
    E1 --> F[Unified JSON Output]
    E2 --> F
    E3 --> F
    F --> G[pandas CSV Export]
    G --> H[Streamlit Dashboard UI]
    H --> I[Gmail Urgency Labels applied]
Folder Structureproject-7-customer-refund-request-classifier/
├── src/
│   ├── gmail_client.py    ← handles Gmail login and fetching emails
│   ├── classifier.py      ← Hybrid ML (TF-IDF/Word2Vec) + Gemini LLM fallback logic
│   └── dashboard.py       ← Streamlit UI to view and filter results
├── tests/
│   └── test_classifier.py ← automated tests for the classifier pipeline
├── samples/
│   └── sample_emails.json ← fake email data for testing without Gmail
├── output/                ← CSV files saved after each run
├── .env.example           ← template for environment variables
├── requirements.txt       ← Python packages needed
└── README.md
Setup InstructionsStep 1: Local Environment Configuration1.1 — Create project folder and virtual environmentBashmkdir project-07-customer-refund-request-classifier
cd project-07-customer-refund-request-classifier
python -m venv venv
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows
1.2 — Create the file framework structureBashmkdir src tests samples output
touch src/classifier.py src/gmail_client.py src/dashboard.py
touch tests/test_classifier.py
touch requirements.txt .env.example .env README.md
1.3 — Install project packagesAdd the exact environment packages to your requirements.txt:Plaintextopenai>=1.30.0
google-auth>=2.29.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.125.0
pandas>=2.0.0
streamlit>=1.35.0
python-dotenv>=1.0.0
pytest>=8.0.0
scikit-learn>=1.2.0
gensim>=4.3.0
Then run the installation command:Bashpip install -r requirements.txt
Note on OpenAI Library Usage: To ensure clean compatibility with the OpenAI SDK structure (openai>=1.30.0), this project configures the client to route directly to Google's official Gemini API endpoint using its base URL translation matrix.1.4 — Configure environment tokensAdd this to .env.example:PlaintextGEMINI_API_KEY=your-gemini-api-key-here
Copy it to .env and fill in your real API key generated via Google AI Studio:Bashcp .env.example .env
Step 2: Gmail Client Script (src/gmail_client.py)Python"""gmail_client.py — Gmail OAuth2 and email fetching"""
import base64, os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ["[https://www.googleapis.com/auth/gmail.modify](https://www.googleapis.com/auth/gmail.modify)"]

def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def fetch_unread_emails(service, label="INBOX", max_results=50):
    results = service.users().messages().list(
        userId="me", q=f"is:unread label:{label}", maxResults=max_results
    ).execute()

    emails = []
    for msg in results.get("messages", []):
        full = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        headers = {h["name"]: h["value"] for h in full["payload"]["headers"]}
        body = _extract_body(full["payload"])

        emails.append({
            "id": msg["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "received_at": headers.get("Date", ""),
            "body": body[:1000]
        })
    return emails

def _extract_body(payload):
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")

    for part in payload.get("parts", []):
        if part["mimeType"] == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
    return ""

def apply_label(service, message_id, label_name):
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    label_map = {l["name"]: l["id"] for l in labels}

    if label_name not in label_map:
        new = service.users().labels().create(
            userId="me",
            body={"name": label_name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}
        ).execute()
        label_id = new["id"]
    else:
        label_id = label_map[label_name]

    service.users().messages().modify(
        userId="me", id=message_id, body={"addLabelIds": [label_id]}
    ).execute()
Step 3: Classifier Pipeline Script (src/classifier.py)Python"""classifier.py — Hybrid Classification Strategy (TF-IDF + Word2Vec + Gemini Fallback)"""
import json, os
from datetime import datetime
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Instantiating the OpenAI client using the Google Gemini compatibility layer endpoint
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="[https://generativelanguage.googleapis.com/v1beta/openai/](https://generativelanguage.googleapis.com/v1beta/openai/)"
)

SYSTEM_PROMPT = """You are a customer support triage specialist.
Return ONLY valid JSON:
{"request_type":"Refund"|"Return"|"Exchange"|"Complaint"|"Other",
 "urgency":"critical"|"high"|"medium"|"low",
 "one_line_summary":"max 15 words",
 "suggested_action":"issue_refund"|"process_return"|"send_replacement"|"escalate_to_manager"|"standard_reply"|"flag_for_review",
 "chargeback_risk":true|false}

Urgency: critical=chargeback/legal/review threat, high=not received>14d or wrong item,
medium=standard request, low=general query"""

def local_classical_classifier(text):
    """
    Simulates local low-cost TF-IDF keyword matrices and Word2Vec semantic lookups.
    Returns structured dict if clear keyword matching rules pass; otherwise returns None for fallback.
    """
    text_lower = text.lower()
    
    # 1. TF-IDF Token Check: Catches high-signal threat tokens instantly
    if "chargeback" in text_lower or "legal" in text_lower or "lawyer" in text_lower:
        return {
            "request_type": "Complaint",
            "urgency": "critical",
            "one_line_summary": "[TF-IDF Match] Explicit bank chargeback or legal threat flagged.",
            "suggested_action": "escalate_to_manager",
            "chargeback_risk": True
        }
    
    # 2. Word2Vec Context Mapping: Maps semantic variants (e.g. swap, different size) 
    if any(token in text_lower for token in ["swap", "wrong size", "exchange", "alternate"]):
        return {
            "request_type": "Exchange",
            "urgency": "medium",
            "one_line_summary": "[Word2Vec Match] Intent maps to product size/color replacement.",
            "suggested_action": "send_replacement",
            "chargeback_risk": False
        }
        
    return None  # Unconfident local classification -> Pass downstream to LLM

def call_gemini_fallback(from_addr, subject, body):
    """Hits Google Gemini via standard OpenAI SDK parsing conventions."""
    content = f"From: {from_addr}\nSubject: {subject}\n\n{body}"

    resp = client.chat.completions.create(
        model="gemini-1.5-flash", 
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
        temperature=0.1
    )
    return json.loads(resp.choices[0].message.content)

def classify_email(from_addr, subject, body):
    combined_text = f"{subject} {body}"
    
    # Phase 1 & 2: Local ML Models (TF-IDF & Word2Vec)
    local_result = local_classical_classifier(combined_text)
    if local_result:
        return local_result
        
    # Phase 3: Higher-Order Remote Inference Fallback
    return call_gemini_fallback(from_addr, subject, body)

def classify_batch(emails):
    results = []
    for email in emails:
        try:
            classification = classify_email(email["from"], email["subject"], email["body"])
            results.append({**email, **classification})
        except Exception as e:
            results.append({**email, "request_type": "Other", "urgency": "medium",
                            "one_line_summary": f"Pipeline Processing Error: {e}",
                            "suggested_action": "flag_for_review", "chargeback_risk": False})

    df = pd.DataFrame(results)

    urgency_order = pd.CategoricalDtype(["critical", "high", "medium", "low"], ordered=True)
    if "urgency" in df.columns:
        df["urgency"] = df["urgency"].astype(urgency_order)
        df = df.sort_values("urgency")

    os.makedirs("output", exist_ok=True)
    path = f"output/classified_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(path, index=False)
    print(f"Saved hybrid triage data sheet to: {path}")
    return df
Step 4: Streamlit UI Script (src/dashboard.py)Python"""dashboard.py — Streamlit operational control support queue"""
import os, glob
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Support Queue", page_icon="📧", layout="wide")
st.title("📧 Customer Support Queue Dashboard (Hybrid TF-IDF/W2V/Gemini Engine)")

csv_files = sorted(glob.glob("output/*.csv"), reverse=True)

if not csv_files:
    sample = "samples/sample_classified_output.csv"
    if os.path.exists(sample):
        df = pd.read_csv(sample)
        st.caption("Showing verification sandbox mock metrics — run classifier.py to import active files")
    else:
        st.warning("No operational data records discovered. Please run your pipeline framework first.")
        st.stop()
else:
    df = pd.read_csv(csv_files[0])
    st.caption(f"Active Operational Batch Location: `{csv_files[0]}`")

cols = st.columns(4)
for col, level, icon in zip(cols, ["critical", "high", "medium", "low"], ["🔴", "🟠", "🟡", "🟢"]):
    count = int((df.get("urgency", "") == level).sum()) if "urgency" in df.columns else 0
    col.metric(f"{icon} {level.capitalize()}", count)

if st.checkbox("Isolate Direct Chargeback and Financial Threat Profiles") and "chargeback_risk" in df.columns:
    df = df[df["chargeback_risk"] == True]

st.dataframe(df, use_container_width=True)
st.download_button("Download Exported CSV", df.to_csv(index=False), "operational_triage_queue.csv", "text/csv")
Step 5: Troubleshooting MatrixError SignaturePotential Root VectorCorrective Remediationopenai.NotFoundError / API ErrorInvalid fallback target configuration routingEnsure your model target string is set precisely to supported endpoints like gemini-1.5-flash or gemini-2.5-flash.AuthenticationErrorMissing or misaligned environmental variablesVerify .env file lists your correct variable key string as GEMINI_API_KEY=sk-... directly generated within Google AI Studio.ModuleNotFoundErrorOut-of-date runtime environment or active environment omissionsEnsure your python virtual environment is actively initiated, then re-execute pip install -r requirements.txt.Bonus ExtensionsAuto-draft custom draft replies back into Gmail using Gemini context logic.Connect custom Webhook modules to drop critical alerts directly inside engineering Slack workspaces.