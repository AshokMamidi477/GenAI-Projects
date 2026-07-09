"""
classifier.py

Google Gemini AI async clause classification.
Replaces Anthropic Claude classifier.
"""

import asyncio
import json
import os

import google.generativeai as genai
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Configure Gemini API
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


# Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)


SYSTEM_PROMPT = """
You are a legal document analyst.

Your task is to classify a contract clause into exactly one category.

Available categories:

1. Obligation
A clause describing something a party must do or must not do.

2. Risk/Liability
Clauses involving indemnification, damages,
warranties, representations, or limitations of liability.

3. IP/Ownership
Clauses involving intellectual property,
copyrights, trademarks, licenses, inventions,
or ownership rights.

4. Termination
Clauses related to ending an agreement,
termination rights, notice periods,
or agreement survival.

5. Standard Boilerplate
General legal clauses such as:
- governing law
- confidentiality
- notices
- entire agreement
- definitions

Return ONLY valid JSON.

Format:

{
    "category": "One category name",
    "confidence": 0.0,
    "reasoning": "One sentence explanation"
}
"""


async def classify_clause(index: int, text: str):
    """
    Classifies a single contract clause using Gemini.
    """

    prompt = f"""
{SYSTEM_PROMPT}

Contract Clause:

{text[:2000]}
"""


    try:

        response = await model.generate_content_async(
            prompt
        )


        result_text = response.text.strip()


        # Gemini may wrap JSON in markdown
        if result_text.startswith("```"):
            result_text = (
                result_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


        result = json.loads(result_text)


        return {
            "clause_number": index,
            "clause_text": text,
            "category": result.get(
                "category",
                "Standard Boilerplate"
            ),
            "confidence": float(
                result.get(
                    "confidence",
                    0.5
                )
            ),
            "reasoning": result.get(
                "reasoning",
                ""
            )
        }


    except Exception as e:

        # Safe fallback if Gemini response parsing fails
        return {
            "clause_number": index,
            "clause_text": text,
            "category": "Standard Boilerplate",
            "confidence": 0.0,
            "reasoning": f"Gemini classification failed: {str(e)}"
        }



async def classify_all(clauses):
    """
    Classifies multiple clauses concurrently.

    Example:
    
    Clause 1 ----\
    Clause 2 ----- > Gemini Parallel Requests
    Clause 3 ----/

    """

    tasks = [
        classify_clause(
            clause["index"],
            clause["text"]
        )
        for clause in clauses
    ]


    results = await asyncio.gather(
        *tasks
    )


    return results