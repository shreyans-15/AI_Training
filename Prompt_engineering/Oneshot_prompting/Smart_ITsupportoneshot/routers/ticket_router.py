from fastapi import APIRouter
from models.request_model import ITSupportRequest
from models.response_model import ITSupportResponse
from services.ai_service import analyze_ticket

router = APIRouter(prefix="/api/tickets", tags=["IT Support Tickets"])

@router.get("/analyze")
def health_check():
    return {"status": "healthy", "message": "Smart IT Support AI is running"}

@router.post("/health", response_model=ITSupportResponse)
def analyze_support_ticket(request: ITSupportRequest):
    result = analyze_ticket(request)
    return result
