from pydantic import BaseModel, Field, field_validator
from typing import Literal

# Model 1 : input
class AstronautRequest(BaseModel):

    astronaut_id: str = Field(min_length = 1)
    astronaut_name: str = Field(min_length = 1)
    age: int = Field(ge=18, le=65)
    training_hours: int = Field(ge=0)
    medical_clearance: bool
    previous_missions: int = Field(ge=0)
    mission_type: Literal["Research", "Maintenance", "Exploration"]

    #reject values that contain only spaces
    @field_validator("astronaut_id", "astronaut_name")
    @classmethod
    def must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()

# Model 2 : internal analysis 
class AstronautAnalysis(BaseModel):

    age_eligible: bool
    training_eligible: bool
    medical_eligible: bool
    experience_eligible: bool
    failed_checks: list[str]
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]

# Model 3 : final output (also the schema given to with_structured_output)
class AstronautResponse(BaseModel):

    astronaut_id: str
    astronaut_name: str
    mission_type: str
    readiness_status: Literal["READY", "NOT_READY"]
    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    reason: str
    recommendation: str
