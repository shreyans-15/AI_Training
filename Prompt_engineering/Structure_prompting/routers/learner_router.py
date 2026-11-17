from fastapi import APIRouter
from models.ai_model import LearnerRequest, LearnerResponse
from services.llm_service import analyse_learner

router = APIRouter(prefix = "/api/learners", tags = ["Learners"])

@router.post("/analyse", response_model = LearnerResponse)
def analyze_learner_performance(learner: LearnerRequest):
    """
    Analyze the performance of a learner based on their scores, attendance, and assignment completion.
    Returns a detailed analysis including average score, performance level, strongest and weakest technology,
    technical assessment, and recommended learning resources.
    """
    return analyse_learner(learner)