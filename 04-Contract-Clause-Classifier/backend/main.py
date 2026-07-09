"""main.py — FastAPI app"""
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import ClassifyRequest, ClassifyResponse, ClauseResult
from backend.segmenter import split_into_clauses
from backend.classifier import classify_all

app = FastAPI(title="Contract Clause Classifier")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest):
    if len(req.text.strip()) < 100:
        raise HTTPException(422, "Contract text too short.")
    start = time.time()
    clauses = split_into_clauses(req.text)
    if not clauses:
        raise HTTPException(422, "No clauses identified.")
    results = await classify_all(clauses)
    return ClassifyResponse(
        clauses=[ClauseResult(**r) for r in results],
        total_clauses=len(results),
        processing_time_ms=int((time.time() - start) * 1000),
    )
