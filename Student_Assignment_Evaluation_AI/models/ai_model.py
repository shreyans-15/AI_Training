from pydantic import BaseModel, Field
 
class StudentAssignmentRequest(BaseModel):
    student_name: str = Field(..., min_length=1)
    course_name: str = Field(..., min_length=1)
    assignment_title: str = Field(..., min_length=1)
    assignment_description: str = Field(..., min_length=1)
    evaluation_criteria: list[str]
 
class StudentAssignmentResponse(BaseModel):
    student_name: str
    overall_assessment: str
    demonstrated_skills: list[str]
    gaps_or_missing_evidence: list[str]
    improvement_suggestions: list[str]
    next_practice_tasks: list[str]
    feedback_summary: str
 