from models.ai_model import RequestFromAI, ResponseFromAI
from service.llm_service import generate_ai_response
from fastapi import FastAPI

app = FastAPI(
    title = "AI Text Assistant",
    version = "1.1"
)

@app.get("/")
def home():
    return {
        "message": "AI text assistant is working"
    }

@app.post("/api/v1/generate",response_model = ResponseFromAI)
def generate_text(request: RequestFromAI): 
    result = generate_ai_response(request)
    return result