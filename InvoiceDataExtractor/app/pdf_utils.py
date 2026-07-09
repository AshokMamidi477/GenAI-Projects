"""pdf_utils.py — converts PDF pages to base64 images"""

import base64
import fitz   # PyMuPDF — imported as 'fitz' even though the package is called pymupdf

MAX_PAGES = 3       # Only process the first 3 pages — invoices are rarely longer
RENDER_SCALE = 2.0  # Render at 2× resolution for better OCR accuracy on scanned docs


def pdf_to_base64_images(pdf_bytes: bytes) -> list[str]:
    """Convert the first MAX_PAGES pages to base64 JPEG strings."""
    # Open the PDF from raw bytes (not a file path)
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    if doc.is_encrypted:
        raise ValueError("This PDF is password-protected. Please provide an unlocked version.")

    images = []
    matrix = fitz.Matrix(RENDER_SCALE, RENDER_SCALE)   # Scale matrix for rendering

    for page_num in range(min(len(doc), MAX_PAGES)):
        page = doc[page_num]
        pixmap = page.get_pixmap(matrix=matrix)     # Render the page to pixels
        jpeg_bytes = pixmap.tobytes("jpeg")          # Convert pixels to JPEG bytes
        b64 = base64.b64encode(jpeg_bytes).decode("utf-8")  # Encode as base64 string
        images.append(b64)

    doc.close()
    return images

def build_vision_content(b64_images: list[str]) -> list[dict]:
    """Build the content array for the OpenAI Vision API call."""
    content = []
    for i, b64 in enumerate(b64_images):
        # Label each page so GPT knows which page it's looking at
        content.append({"type": "text", "text": f"Page {i + 1} of the invoice:"})
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64}",
                "detail": "high",   # "high" = better accuracy, more tokens; "low" = faster, cheaper
            }
        })
    return content

