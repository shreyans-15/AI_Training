from pydantic import BaseModel, Field


class LearnerProgressAnalysis(BaseModel):
    completion_percentage: float = Field(..., ge=0, le=100)
    learning_level: str
    strong_topics: list[str]
    weak_topics: list[str]
    readiness_score: float = Field(..., ge=0, le=100)
    improvement_priority: str
