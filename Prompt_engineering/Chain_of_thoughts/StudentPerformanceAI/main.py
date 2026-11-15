from fastapi import FastAPI
from services.llm_service import analyze_student_performance
from models.student_model import StudentPerformanceAnalysis,StudentPerformanceRequest,StudentPerformanceResponse
 
app= FastAPI(title="Student Performance Analysis",version = "1.0.0")
 
@app.get("/")
def home():
    return{
        "message":"Student Analyzer is working"
    }
 
 
@app.post("/api/v1/analyze_student",response_model = StudentPerformanceResponse)
def student_analyzer(
    request:StudentPerformanceRequest
):
    return analyze_student_performance(request)
