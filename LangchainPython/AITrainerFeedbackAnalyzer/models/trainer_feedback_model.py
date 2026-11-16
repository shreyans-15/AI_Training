from pydantic import BaseModel, Field
from typing import Literal

class TrainerFeedbackRequest(BaseModel):

    trainer_name: str
    training_topic: str
    learner_name: str
    rating: int = Field(ge=1, le=5)
    feedback: str

class TrainerFeedbackResponse(BaseModel):

    trainer_name: str
    sentiments: Literal["Positive", "Negative", "Neutral"]  
    performance_level: Literal["Excellent", "Good", "Average", "Needs Improvement"]  
    strengths: list[str]
    improvement_areas: list[str]
    recomendations: str
    overall_summary: str
    