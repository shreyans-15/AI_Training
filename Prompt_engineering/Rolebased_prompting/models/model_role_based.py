from pydantic import BaseModel , Field
from typing import Literal

class PythonAIRequest(BaseModel): # request model which defines the data,user must send to the API.
    learner_name: str
    question: str
    experience_level: Literal["Fresher","Intermediate","Experienced"]

class PythonAIResponse(BaseModel):
    learner_name: str
    role: str
    answer: str