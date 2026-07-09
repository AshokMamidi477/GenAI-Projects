"""models.py — Pydantic schemas"""
from typing import Literal, List
from pydantic import BaseModel

CATEGORIES = Literal[
    "Obligation", "Risk/Liability", "IP/Ownership",
    "Standard Boilerplate", "Termination",
]

class ClassifyRequest(BaseModel):
    text: str

class ClauseResult(BaseModel):
    clause_number: int
    clause_text: str
    category: CATEGORIES
    confidence: float
    reasoning: str

class ClassifyResponse(BaseModel):
    clauses: List[ClauseResult]
    total_clauses: int
    processing_time_ms: int
