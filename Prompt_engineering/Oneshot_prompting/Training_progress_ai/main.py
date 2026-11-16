from fastapi import FastAPI
from routers.analysis_router import router as analysis_router

app = FastAPI(title="Training Progress Analyzer")
app.include_router(analysis_router)
