"""models.py"""
from typing import List, Literal, Optional
from pydantic import BaseModel

class Medication(BaseModel):
    name: str
    dose: Optional[str] = None
    frequency: Optional[str] = None
    purpose: Optional[str] = None

class GenerateRequest(BaseModel):
    note: str
    reading_level: Literal["5th grade", "8th grade", "adult"]
    patient_name: str = "Patient"

class InstructionResponse(BaseModel):
    what_happened: Optional[str] = None
    medications: List[Medication] = []
    home_care_instructions: List[str] = []
    warning_signs: List[str] = []
    followup: Optional[str] = None
