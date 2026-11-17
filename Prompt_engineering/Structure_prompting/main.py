from fastapi import FastAPI
from routers.learner_router import router as learner_router

app = FastAPI(

    title="Learner Performance Analysis API",
    description="AI-assisted corporate training performance analyzer",
    version="1.0.0",
)

app.include_router(learner_router)

@app.get("/")
def home():
    return {"message":"Training performance AI is running"}