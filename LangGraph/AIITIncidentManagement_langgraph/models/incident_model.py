from pydantic import BaseModel, Field
from typing import Literal

class IncidentRequest(BaseModel):

    employee_id: str
    employee_name: str
    department: str
    issue: str = Field(min_length = 5)

# LangChain structured output schema (what the LLM must return)
class IncidentAnalysis(BaseModel):

    category: Literal["Network", "Application", "Password", "Server", "Database", "Other"]
    priority: Literal["Critical", "High", "Medium", "Low"]
    summary: str
    business_impact: str
    suggested_resolution: str

# Final API response
class IncidentResponse(BaseModel):

    employee_id: str
    employee_name: str
    category: str
    priority: str
    summary: str
    suggested_resolution: str
    escalation_required: bool
    email_sent: bool
    email_message: str
    status: str
