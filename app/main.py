from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from app.career_mentor import run_career_mentor

app = FastAPI(
    title="We-KIT AI Services",
    description="AI-powered psychometric and career mentoring services for We-KIT",
    version="1.0.0"
)

class CareerMentorRequest(BaseModel):
    age: int
    interests: List[str]
    strengths_summary: str | None = None
    values_summary: str | None = None
    context: str = "India"


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/psychometrics/career-mentor")
def career_mentor_endpoint(payload: CareerMentorRequest):
    try:
        return run_career_mentor(
            age=payload.age,
            interests=payload.interests,
            strengths_summary=payload.strengths_summary,
            values_summary=payload.values_summary,
            context=payload.context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
