from pydantic import BaseModel, Field
from typing import Literal

class EmployeeRequest(BaseModel):

    employee_id: int
    employee_name: str = Field(min_length = 1)
    department: str
    designation: str
    experience: float = Field(ge=0)
    technical_skills: list[str]
    performance_rating: float = Field(ge=1, le=5)
    attendance_percentage: float = Field(ge=0, le=100)
    projects_completed: int = Field(ge=0)
    manager_feedback: str

class BatchEmployeeRequest(BaseModel):

    employees: list[EmployeeRequest] = Field(min_length = 1)

class EmployeeResponse(BaseModel):

    employee_id: int
    employee_name: str
    performance_level: Literal["Excellent", "Good", "Average", "Needs Improvement"]
    strengths: list[str]
    improvement_areas: list[str]
    training_recommendations: list[str]
    promotion_readiness: Literal["Ready", "Needs Development", "Not Ready"]
    ai_feedback: str
    recommended_action: str

class BatchEmployeeResponse(BaseModel):

    total_employees: int
    results: list[EmployeeResponse]
