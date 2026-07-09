"""main.py — FastAPI"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import GenerateRequest, InstructionResponse
from backend.generator import generate_instructions

app = FastAPI(title="Discharge Instruction Generator")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/generate-instructions", response_model=InstructionResponse)
def generate(req: GenerateRequest):
    if len(req.note.strip()) < 50:
        raise HTTPException(422,"Note too short (min 50 chars).")
    try:
        return generate_instructions(req.note, req.reading_level, req.patient_name)
    except Exception as e:
        raise HTTPException(500, str(e))
