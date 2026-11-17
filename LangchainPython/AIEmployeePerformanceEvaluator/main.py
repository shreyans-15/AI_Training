from fastapi import FastAPI
from services.llm_service import evaluate_employees
from models.employee_model import BatchEmployeeRequest,BatchEmployeeResponse

app = FastAPI(
    title="AIEmployeePerformanceEvaluator"
)

@app.get("/")
def home():
    return{
        "message":"AI Employee Performance Evaluator"
    }

@app.post("/api/v1/employees/batch-evaluation",response_model = BatchEmployeeResponse)
def batch_evaluation(
    request:BatchEmployeeRequest
):
    return evaluate_employees(request)
