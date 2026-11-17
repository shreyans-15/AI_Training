from pydantic import BaseModel, Field
from typing import Literal

class HelpdeskRequest(BaseModel):

    employeeId: set
    employeeName: str
    issue: str = Field(min_length = 5)

class HelpdeskResponse(BaseModel):

    employeeId: str
    category: str
    priority: str
    agentUsed: str
    toolsCalled: list[str]
    resolution: list[str]
    reviewStatus: str
    ticketId: str | None = None
    status: str

