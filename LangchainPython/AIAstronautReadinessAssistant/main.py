from fastapi import FastAPI, HTTPException
from services.llm_service import analyze_astronaut, analyze_astronauts
from models.astronaut_model import AstronautRequest,AstronautResponse

app = FastAPI(
    title="AIAstronautReadinessAssistant"
)

#Normal chain : one astronaut
@app.post("/api/v1/astronaut-readiness",response_model = AstronautResponse)
def astronaut_readiness(
    request:AstronautRequest
):
    return analyze_astronaut(request)

#Batch processing : list of astronauts
@app.post("/api/v1/astronaut-readiness/batch",response_model = list[AstronautResponse])
def astronaut_readiness_batch(
    requests:list[AstronautRequest]
):
    if not requests:
        raise HTTPException(
            status_code=400,
            detail="Send at least one astronaut"
        )

    return analyze_astronauts(requests)
