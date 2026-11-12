from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class TrainingFeedbackBase(BaseModel):
    learner_name: str = Field(min_length=1, max_length=100)
    trainer_name: str = Field(min_length=1, max_length=100)
    course_name: str = Field(min_length=1, max_length=150)
    session_date: date
    content_rating: int = Field(ge=1, le=5)
    trainer_rating: int = Field(ge=1, le=5)
    hands_on_rating: int = Field(ge=1, le=5)
    comments: Optional[str] = Field(default=None, max_length=1000)
    would_recommend: bool

class TrainingFeedbackCreate(TrainingFeedbackBase):
    feedback_id: int = Field(gt=0)

class TrainingFeedbackUpdate(BaseModel):
    learner_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    trainer_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    course_name: Optional[str] = Field(default=None, min_length=1, max_length=150)
    session_date: Optional[date] = None
    content_rating: Optional[int] = Field(default=None, ge=1, le=5)
    trainer_rating: Optional[int] = Field(default=None, ge=1, le=5)
    hands_on_rating: Optional[int] = Field(default=None, ge=1, le=5)
    comments: Optional[str] = Field(default=None, max_length=1000)
    would_recommend: Optional[bool] = None

class TrainingFeedbackResponse(TrainingFeedbackBase):
    feedback_id: int
    model_config = ConfigDict(from_attributes=True)
