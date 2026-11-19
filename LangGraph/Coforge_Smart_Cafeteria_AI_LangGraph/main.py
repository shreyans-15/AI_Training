from fastapi import FastAPI
from routers.cafeteria_router import router as cafeteria_router

app = FastAPI(
    title="Coforge Smart Cafeteria AI",
    description=(
        "Food ordering, invoice generation and delay escalation "
        "using FastAPI, LangChain and LangGraph."
    ),
    version="1.0.0"
)

app.include_router(cafeteria_router)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
