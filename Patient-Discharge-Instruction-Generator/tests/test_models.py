"""test_models.py"""
import sys; sys.path.insert(0,".")
from backend.models import InstructionResponse, Medication

def test_medication_dose_optional():
    m = Medication(name="Ibuprofen")
    assert m.dose is None

def test_response_defaults():
    r = InstructionResponse()
    assert r.medications == []
    assert r.home_care_instructions == []

def test_full_response():
    r = InstructionResponse(
        what_happened="You had pneumonia.",
        medications=[Medication(name="Amoxicillin",dose="500mg",frequency="3x daily")],
        home_care_instructions=["Rest","Drink fluids"],
        warning_signs=["Difficulty breathing"],
        followup="Call your GP in one week.",
    )
    assert len(r.medications)==1
    assert r.medications[0].name=="Amoxicillin"
