from pydantic import BaseModel, Field    #pydantic used for data validation

class EmployeeFeedbackRequest(BaseModel):
 
    employee_name: str = Field(..., min_length=1)
    reviewer_name: str = Field(..., min_length=1)
    project_name: str = Field(..., min_length=1)
    performance_rating: int = Field(..., ge=1, le=5)
    feedback: str = Field(..., min_length=1)
 
class EmployeeFeedbackResponse(BaseModel):
 
    employee_name: str
    sentiment: str
    performance_level: str
    strengths: list[str]
    improvement_areas: list[str]
    development_recommendations: list[str]
    overall_summary: str
    suggested_action: str