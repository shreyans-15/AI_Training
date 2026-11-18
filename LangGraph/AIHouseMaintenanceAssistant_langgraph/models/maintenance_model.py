from pydantic import BaseModel, Field

class MaintenanceRequest(BaseModel):

    question: str = Field(min_length = 3)

# LangChain structured output schema (what the LLM must return)
class MaintenanceAnswer(BaseModel):

    answer: str

# Final API response
class MaintenanceResponse(BaseModel):

    question: str
    answer: str
