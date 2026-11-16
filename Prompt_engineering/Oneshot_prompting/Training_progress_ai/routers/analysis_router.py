from fastapi import APIRouter

from models.request_model import LearnerProgressRequest
from models.response_model import LearnerProgressResponse
from services.ai_service import analyze_learner_progress

router = APIRouter(prefix="/api/training", tags=["Training Progress"])


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Training Progress Analyzer is running",
    }


@router.post("/analyze-progress", response_model=LearnerProgressResponse)
def analyze_progress(request: LearnerProgressRequest):
    result = analyze_learner_progress(request)
    return result
