"""gmail_client.py — Gmail OAuth2 and email fetching"""

import base64
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# This scope allows reading AND modifying emails (needed to apply labels)
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


def get_gmail_service():
    """Authenticate and return a Gmail API service instance."""

    creds = None

    # Load existing token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Refresh or create new credentials
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        # Save token for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


def fetch_unread_emails(service, label="INBOX", max_results=50):
    """
    Fetch unread emails from Gmail.

    Returns:
    [
        {
            id,
            subject,
            from,
            received_at,
            body
        }
    ]
    """

    results = service.users().messages().list(
        userId="me",
        labelIds=[label],
        q="is:unread",
        maxResults=max_results
    ).execute()

    messages = results.get(
        "messages",
        []
    )

    email_data = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"]
        ).execute()

        payload = msg.get(
            "payload",
            {}
        )

        # Convert headers list into dictionary
        headers = {
            header["name"]: header["value"]
            for header in payload.get("headers", [])
        }

        body = _extract_body(payload)

        email_data.append(
            {
                "id": message["id"],
                "subject": headers.get("Subject", ""),
                "from": headers.get("From", ""),
                "received_at": headers.get("Date", ""),
                "body": body[:1000]
            }
        )

    return email_data


def _extract_body(payload):
    """
    Extract email body from Gmail payload.

    Handles:
    - Simple text emails
    - Multipart emails
    - HTML + text emails
    - Nested multipart messages
    """

    # Simple email body
    if payload.get("body", {}).get("data"):

        return base64.urlsafe_b64decode(
            payload["body"]["data"]
        ).decode(
            "utf-8",
            errors="ignore"
        )


    # Multipart email
    for part in payload.get("parts", []):

        mime_type = part.get(
            "mimeType",
            ""
        )

        # Prefer plain text
        if mime_type == "text/plain":

            data = part.get(
                "body",
                {}
            ).get(
                "data"
            )

            if data:
                return base64.urlsafe_b64decode(
                    data
                ).decode(
                    "utf-8",
                    errors="ignore"
                )


        # Handle nested multipart
        if part.get("parts"):

            nested_body = _extract_body(part)

            if nested_body:
                return nested_body


    return ""


def get_or_create_label(service, label_name):
    """
    Get Gmail label ID.
    Creates label if it does not exist.
    """

    labels = service.users().labels().list(
        userId="me"
    ).execute().get(
        "labels",
        []
    )

    label_map = {
        label["name"]: label["id"]
        for label in labels
    }


    if label_name in label_map:
        return label_map[label_name]


    new_label = service.users().labels().create(
        userId="me",
        body={
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
    ).execute()


    return new_label["id"]


def apply_label(service, message_id, label_name):
    """
    Apply Gmail label to a message.
    """

    label_id = get_or_create_label(
        service,
        label_name
    )

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "addLabelIds": [
                label_id
            ]
        }
    ).execute()