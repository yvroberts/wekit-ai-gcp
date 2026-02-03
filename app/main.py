from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.career_mentor import run_career_mentor

# ---------------------------------------------------------
# FastAPI app definition
# ---------------------------------------------------------
app = FastAPI(
    title="We-KIT AI Services",
    description="AI-powered psychometric and career mentoring services for We-KIT",
    version="1.0.0"
)

# ---------------------------------------------------------
# Request schema (Pydantic v1 compatible)
# ---------------------------------------------------------
class CareerMentorRequest(BaseModel):
    age: int
    interests: List[str]
    strengths_summary: Optional[str] = None
    values_summary: Optional[str] = None
    context: str = "India"


# ---------------------------------------------------------
# Health check (required for Cloud Run)
# ---------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------------------------------------------------
# Main AI endpoint
# ---------------------------------------------------------
@app.post("/psychometrics/career-mentor")
def career_mentor_endpoint(payload: CareerMentorRequest):
    try:
        result = run_career_mentor(
            age=payload.age,
            interests=payload.interests,
            strengths_summary=payload.strengths_summary,
            values_summary=payload.values_summary,
            context=payload.context
        )
        return result

    except ValueError as ve:
        # Handles JSON parsing or model output errors
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # Catch-all for unexpected failures
        raise HTTPException(status_code=500, detail="Internal AI service error")
        
