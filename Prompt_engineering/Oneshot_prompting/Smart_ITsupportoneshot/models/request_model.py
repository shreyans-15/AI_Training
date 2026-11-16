from pydantic import BaseModel, Field


class ITSupportRequest(BaseModel):
    ticket_id: str = Field(..., min_length=1)
    employee_id: str = Field(..., min_length=1)
    employee_name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    issue_description: str = Field(..., min_length=1)
    affected_system: str = Field(..., min_length=1)
