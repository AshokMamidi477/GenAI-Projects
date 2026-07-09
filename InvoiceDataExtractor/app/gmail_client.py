"""gmail_client.py — Gmail API integration for fetching invoice attachments."""

import base64
import os
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Gmail API scopes — read-only access to messages
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Paths for OAuth credentials
CREDENTIALS_DIR = Path(__file__).parent.parent / "credentials"
CLIENT_SECRET_FILE = CREDENTIALS_DIR / "client_secret.json"
TOKEN_FILE = CREDENTIALS_DIR / "token.json"


def get_gmail_service():
    """Authenticate and return a Gmail API service instance."""
    creds = None

    # Load existing token if available
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                raise FileNotFoundError(
                    f"OAuth client secret not found at {CLIENT_SECRET_FILE}. "
                    "Download it from Google Cloud Console → APIs & Services → Credentials."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=8090, open_browser=True)

        # Save token for future use
        CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def search_emails(service, query: str = "has:attachment filename:pdf subject:invoice", max_results: int = 10):
    """Search Gmail for messages matching the query."""
    results = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    return messages


def get_message_details(service, msg_id: str) -> dict:
    """Get message metadata (subject, sender, date)."""
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="metadata",
        metadataHeaders=["Subject", "From", "Date"]
    ).execute()

    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    return {
        "id": msg_id,
        "subject": headers.get("Subject", "(no subject)"),
        "from": headers.get("From", "unknown"),
        "date": headers.get("Date", "unknown"),
    }


def get_pdf_attachments(service, msg_id: str) -> list[dict]:
    """Download PDF attachments from a specific message.
    
    Returns a list of dicts: [{"filename": str, "data": bytes}, ...]
    """
    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    attachments = []
    parts = msg.get("payload", {}).get("parts", [])

    for part in parts:
        filename = part.get("filename", "")
        mime_type = part.get("mimeType", "")

        # Only grab PDF attachments
        if not filename.lower().endswith(".pdf") and mime_type != "application/pdf":
            continue

        body = part.get("body", {})
        attachment_id = body.get("attachmentId")

        if attachment_id:
            # Fetch the actual attachment data
            att = service.users().messages().attachments().get(
                userId="me", messageId=msg_id, id=attachment_id
            ).execute()
            # Gmail returns URL-safe base64
            file_data = base64.urlsafe_b64decode(att["data"])
        elif body.get("data"):
            file_data = base64.urlsafe_b64decode(body["data"])
        else:
            continue

        attachments.append({
            "filename": filename or "attachment.pdf",
            "data": file_data,
        })

    return attachments


def fetch_invoice_emails(query: str = "has:attachment filename:pdf subject:invoice", max_results: int = 10):
    """High-level function: authenticate, search, and return email metadata.
    
    Returns: (service, list of message detail dicts)
    """
    service = get_gmail_service()
    messages = search_emails(service, query=query, max_results=max_results)

    email_details = []
    for msg in messages:
        details = get_message_details(service, msg["id"])
        email_details.append(details)

    return service, email_details
