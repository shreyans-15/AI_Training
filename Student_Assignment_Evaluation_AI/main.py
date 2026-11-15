from models.ai_model import StudentAssignmentRequest, StudentAssignmentResponse
from services.llm_services import evaluate_student_assignment
from fastapi import FastAPI
 
 
app = FastAPI(
    title="Student Assignment Evaluation AI",
    version="1.0"
)
 
 
@app.get("/")
def home():
    return {
        "message": "Student Assignment Evaluation AI is working"
    }
 
 
@app.post("/api/v1/evaluate-assignment", response_model=StudentAssignmentResponse)
def evaluate_assignment(request: StudentAssignmentRequest):
 
    result = evaluate_student_assignment(request)
    return result
 