"""generator.py — Gemini prompt and parsing"""

import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

from backend.models import InstructionResponse, Medication


load_dotenv()


# Configure Gemini API
genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)


EXAMPLES = {
    "5th grade": "You had an infection. The doctors gave you medicine to make it better.",
    "8th grade": "You were treated for a stomach infection. You received fluids and antibiotics.",
    "adult": "You presented with acute gastroenteritis and received IV fluid resuscitation.",
}


def generate_instructions(note, reading_level, patient_name):

    system_prompt = f"""
You are a patient education specialist.

Your task is to convert medical notes into easy-to-understand patient instructions.

Reading level:
{reading_level}

Example writing style:
"{EXAMPLES[reading_level]}"

Patient name:
{patient_name}

Rules:
- Use "you" and "your" throughout.
- Write in a clear, empathetic patient-friendly tone.
- Never invent medication names, dosages, or frequencies.
- If medication dosage is missing, use "as prescribed".
- Do not add medical information that is not present in the note.

Return ONLY valid JSON in this exact format:

{{
    "what_happened": "2-3 sentences explaining what happened",
    "medications": [
        {{
            "name": "",
            "dose": "",
            "frequency": "",
            "purpose": ""
        }}
    ],
    "home_care_instructions": [
        "4-8 items"
    ],
    "warning_signs": [
        "3-6 items"
    ],
    "followup": "one sentence"
}}
"""


    model = genai.GenerativeModel(
        model_name="gemini-3.1-flash-lite",
        system_instruction=system_prompt
    )


    response = model.generate_content(
        f"""
Patient Medical Note:

{note}
""",
        generation_config=genai.GenerationConfig(
            temperature=0.2,
            max_output_tokens=1500,
            response_mime_type="application/json"
        )
    )


    raw = json.loads(response.text)


    raw["medications"] = [
        Medication(**medication)
        if isinstance(medication, dict)
        else Medication(name=str(medication))
        for medication in raw.get("medications", [])
    ]


    return InstructionResponse(**raw)