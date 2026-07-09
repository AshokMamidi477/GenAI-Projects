"""extractor.py — invoice extraction"""

import json, os
import google.generativeai as genai
from dotenv import load_dotenv
from pdf_utils import build_vision_content



load_dotenv()

SYSTEM_PROMPT = """
You are a financial document extraction assistant.
Extract all invoice fields from the provided image(s) and return ONLY a valid JSON object.

JSON SCHEMA:
{
  "vendor_name": "string or null",
  "invoice_number": "string or null",
  "invoice_date": "string in ISO 8601 (YYYY-MM-DD) or null",
  "due_date": "string in ISO 8601 or null",
  "line_items": [
    {
      "description": "string",
      "quantity": "number or null",
      "unit_price": "number or null",
      "total": "number or null"
    }
  ],
  "subtotal": "number or null",
  "tax_amount": "number or null",
  "tax_rate": "string or null (e.g. '20%')",
  "grand_total": "number or null",
  "currency": "3-letter ISO code or null (e.g. USD, GBP, EUR)"
}

RULES:
- If a field is not visible in the document, return null — never guess or calculate
- Treat all pages as one continuous document
- Return ONLY the JSON object — no markdown, no explanation
"""

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
)

# def extract_invoice_For_OpenAI(b64_images: list[str]) -> dict:
#     """Send images to OpenAI and return parsed invoice data."""
#     vision_content = build_vision_content(b64_images)

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         response_format={"type": "json_object"},   # Force valid JSON
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": vision_content},   # vision_content is a list of text+image blocks
#         ],
#         temperature=0.1,    # Very low — extraction should be deterministic
#         max_tokens=1500,    # Enough for a full invoice with many line items
#     )

#     return json.loads(response.choices[0].message.content)

def extract_invoice(b64_images: list[str]) -> dict:
    """Send images to Gemini Vision and return parsed invoice data."""
    import base64

    # Build content parts: convert base64 images to Gemini format
    parts = []
    for b64_image in b64_images:
        # Decode base64 string to raw bytes for the Gemini SDK
        image_bytes = base64.b64decode(b64_image)
        parts.append({"mime_type": "image/jpeg", "data": image_bytes})
    parts.append("Extract the invoice data from the provided image(s) and return ONLY valid JSON.")

    response = model.generate_content(
        contents=parts,
        generation_config=genai.GenerationConfig(
            temperature=0.1,
            max_output_tokens=1500,
            response_mime_type="application/json",
        )
    )

    # Handle blocked or empty responses
    if not response.parts:
        raise ValueError(f"Gemini returned no content. Finish reason: {response.candidates[0].finish_reason}")

    return json.loads(response.text)