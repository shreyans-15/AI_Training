from models.ai_model import EmployeeFeedbackRequest, EmployeeFeedbackResponse
from services.llm_services import analyze_employee_feedback
from fastapi import FastAPI, HTTPException
 
app = FastAPI(
    title="Employee Performance Feedback AI",
    version="1.0"
)
 
 
# Step-1 create home endpoint
@app.get("/")
def home():
    return {
        "message": "Employee Performance Feedback AI is working"
    }
 
 
# Step-2 create employee analysis endpoint
@app.post(
    "/api/v1/analyze-employee",
    response_model=EmployeeFeedbackResponse
)
def analyze_employee(request: EmployeeFeedbackRequest):
 
    try:
        result = analyze_employee_feedback(request)
        return result
 
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
 