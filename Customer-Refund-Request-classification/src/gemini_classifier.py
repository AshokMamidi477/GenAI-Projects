


import json
import os
from datetime import datetime

import pandas as pd
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
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

def classify_email_With_LLM_Model(from_addr, subject, body):

        content = f"""
                    From: {from_addr}
                    Subject: {subject}
                    Email: {body}
                    """
        
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=content,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.1,
                response_mime_type="application/json"
            )
        )

        print(f"Classified email: {subject} — {from_addr}")
        print(f"Response: {response.text}")
        return json.loads(response.text)