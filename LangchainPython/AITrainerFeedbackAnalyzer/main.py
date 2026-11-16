from fastapi import FastAPI
from services.llm_service import analyze_feedback
from models.trainer_feedback_model import TrainerFeedbackResponse,TrainerFeedbackRequest
 
app = FastAPI(
    title="AITrainerFeedbackAnalyzer"
)
 
@app.post("/api/v1/profile-analyzer",response_model = TrainerFeedbackResponse)
def trainer_feedback(
    request:TrainerFeedbackRequest
):
    return analyze_feedback(request)
   
 