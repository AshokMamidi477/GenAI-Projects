"""
notion_writer.py
Saves generated product descriptions to a Notion database.
"""

import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

BLOCK_LIMIT = 2000


def _split_text(text):
    chunks = []
    while len(text) > BLOCK_LIMIT:
        chunks.append(text[:BLOCK_LIMIT])
        text = text[BLOCK_LIMIT:]

    chunks.append(text)
    return chunks


def save_to_notion(product_name, description, tone, meta):
    """Create a Notion database entry. Returns the page URL."""

    page = notion.pages.create(
        parent={
            "database_id": DATABASE_ID
        },
        properties={
            "Product Name": {
                "title": [
                    {
                        "text": {
                            "content": product_name
                        }
                    }
                ]
            },

            "Tone": {
                "rich_text": [
                    {
                        "text": {
                            "content": tone
                        }
                    }
                ]
            },

            "SEO Meta": {
                "rich_text": [
                    {
                        "text": {
                            "content": meta[:2000]
                        }
                    }
                ]
            },

            "Status": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Draft"
                        }
                    }
                ]
            },
        },

        children=[
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": chunk
                            }
                        }
                    ]
                },
            }
            for chunk in _split_text(description)
        ],
    )

    return page.get("url", "")