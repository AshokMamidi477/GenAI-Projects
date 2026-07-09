"""
prompt_templates.py
Tone-specific prompt builders for product description generation.
"""

TONE_PERSONAS = {
    "Professional": (
        "authoritative, benefit-focused, polished. "
        "No slang. Use active voice. Avoid exclamation marks."
    ),
    "Playful": (
        "friendly, natural, human. Use contractions. "
        "Speak directly to the reader. Light humour is acceptable."
    ),
    "Urgency": (
        "action-oriented, creates desire and FOMO. "
        "Use time-sensitivity language. Strong verbs. Direct call to action."
    ),
}


def build_prompt(title, category, features, audience, keywords, tone):
    persona = TONE_PERSONAS[tone]
    return f"""You are a professional e-commerce copywriter. Write a product description.

TONE: {tone} — {persona}

PRODUCT DETAILS:
- Title: {title}
- Category: {category}
- Key features: {features}
- Target audience: {audience}
- Keywords to include: {keywords if keywords else "none specified"}

OUTPUT FORMAT — return exactly two sections, no markdown:
DESCRIPTION:
[150-200 word product description in the specified tone]

META:
[SEO meta description, max 155 characters, starting with the product name]
"""


def parse_response(text):
    """Split model response into (description, meta) tuple."""
    parts = text.split("META:")
    description = parts[0].replace("DESCRIPTION:", "").strip()
    meta = parts[1].strip() if len(parts) > 1 else ""
    if len(meta) > 155:
        meta = meta[:152] + "..."
    return description, meta
