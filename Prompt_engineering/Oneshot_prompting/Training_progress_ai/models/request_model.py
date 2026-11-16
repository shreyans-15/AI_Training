from pydantic import BaseModel, Field, model_validator


class LearnerProgressRequest(BaseModel):
    learner_id: str = Field(..., min_length=1)
    learner_name: str = Field(..., min_length=1)
    training_program: str = Field(..., min_length=1)
    topics_completed: list[str]
    assignments_assigned: int = Field(..., ge=0)
    assignments_completed: int = Field(..., ge=0)
    attendance_percentage: float = Field(..., ge=0, le=100)
    coding_assessment_score: float = Field(..., ge=0, le=100)
    trainer_feedback: str

    @model_validator(mode="after")
    def check_assignment_counts(self):
        if self.assignments_completed > self.assignments_assigned:
            raise ValueError(
                "assignments_completed cannot be greater than assignments_assigned"
            )
        return self
