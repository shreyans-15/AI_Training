from fastapi import FastAPI
from models.training_model import TrainerRequest, TrainerResponse
from workflow.training_workflow import workflow_graph

app = FastAPI(
    title="Trainer Feedback Analyzer AI"
)

@app.post("/analyze-feedback", response_model=TrainerResponse)
def analyze_feedback(request: TrainerRequest):

    result = workflow_graph.invoke(
        {
            "trainer_name": request.trainer_name,
            "learner_name": request.learner_name,
            "trainer_rating": request.trainer_rating,
            "trainer_feedback": request.trainer_feedback,
            "training_topic": request.training_topic
        }
    )

    return TrainerResponse(
        trainer_name = result["trainer_name"],
        sentiments = result["sentiments"],
        performance_level = result["performance_level"],
        strengths = result["strengths"],
        improvement_areas = result["improvement_areas"],
        overall_summary = result["overall_summary"],
        action_taken = result["action_taken"]
    )


@app.get("/health")
def health():
    return {"status": "healthy"}