from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from config.database import Base, engine, get_db
from config.logging_config import logger
from models.trainingfeedback_model import TrainingFeedback
from schemas.trainingfeedback_schema import (
    TrainingFeedbackCreate,
    TrainingFeedbackResponse,
    TrainingFeedbackUpdate,
)
from services import trainingfeedback_service as service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Corporate Training Feedback API",
    description="API to manage learner feedback, trainer quality, and course satisfaction.",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"message": "Corporate Training Feedback API is running"}

def handle_database_error(operation: str):
    logger.exception("Unexpected database error during %s", operation)
    raise HTTPException(status_code=500, detail="An unexpected database error occurred")

@app.post("/feedback/", response_model=TrainingFeedbackResponse, status_code=201)
def submit_feedback(feedback: TrainingFeedbackCreate, db: Session = Depends(get_db)):
    try:
        result = service.create_feedback(db, feedback)
        logger.info("Feedback created successfully. Feedback ID: %s", result.feedback_id)
        return result
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate feedback ID submission: %s", feedback.feedback_id)
        raise HTTPException(status_code=409, detail="Feedback ID already exists")
    except SQLAlchemyError:
        db.rollback()
        handle_database_error("feedback creation")

@app.get("/feedback/", response_model=list[TrainingFeedbackResponse])
def list_feedback(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        return service.get_all_feedback(db, skip, limit)
    except SQLAlchemyError:
        handle_database_error("listing feedback")

@app.get("/feedback/average-trainer-ratings")
def average_trainer_ratings(db: Session = Depends(get_db)):
    try:
        rows = service.get_average_trainer_ratings(db)
        return [
            {"trainer_name": row.trainer_name, "average_trainer_rating": round(float(row.average_trainer_rating), 2)}
            for row in rows
        ]
    except SQLAlchemyError:
        handle_database_error("calculating average trainer ratings")

@app.get("/feedback/low-rated", response_model=list[TrainingFeedbackResponse])
def low_rated_sessions(db: Session = Depends(get_db)):
    try:
        return service.get_low_rated_sessions(db)
    except SQLAlchemyError:
        handle_database_error("finding low-rated sessions")

@app.get("/feedback/recommendation-percentage")
def recommendation_percentage(course_name: str, db: Session = Depends(get_db)):
    try:
        return service.get_recommendation_percentage(db, course_name)
    except SQLAlchemyError:
        handle_database_error("calculating recommendation percentage")

@app.get("/feedback/by-trainer/{trainer_name}", response_model=list[TrainingFeedbackResponse])
def feedback_by_trainer(trainer_name: str, db: Session = Depends(get_db)):
    try:
        return service.get_feedback_by_trainer(db, trainer_name)
    except SQLAlchemyError:
        handle_database_error("filtering feedback by trainer")

@app.get("/feedback/by-course/{course_name}", response_model=list[TrainingFeedbackResponse])
def feedback_by_course(course_name: str, db: Session = Depends(get_db)):
    try:
        return service.get_feedback_by_course(db, course_name)
    except SQLAlchemyError:
        handle_database_error("filtering feedback by course")

@app.get("/feedback/{feedback_id}", response_model=TrainingFeedbackResponse)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    try:
        result = service.get_feedback_by_id(db, feedback_id)
        if result is None:
            logger.warning("Feedback not found. Feedback ID: %s", feedback_id)
            raise HTTPException(status_code=404, detail="Feedback not found")
        return result
    except SQLAlchemyError:
        handle_database_error("retrieving feedback")

@app.put("/feedback/{feedback_id}", response_model=TrainingFeedbackResponse)
def update_feedback(feedback_id: int, feedback: TrainingFeedbackUpdate, db: Session = Depends(get_db)):
    try:
        if not feedback.model_dump(exclude_unset=True):
            raise HTTPException(status_code=422, detail="At least one field must be provided for update")
        result = service.update_feedback(db, feedback_id, feedback)
        if result is None:
            logger.warning("Cannot update missing feedback. Feedback ID: %s", feedback_id)
            raise HTTPException(status_code=404, detail="Feedback not found")
        logger.info("Feedback updated successfully. Feedback ID: %s", feedback_id)
        return result
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        handle_database_error("updating feedback")

@app.delete("/feedback/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    try:
        result = service.delete_feedback(db, feedback_id)
        if result is None:
            logger.warning("Cannot delete missing feedback. Feedback ID: %s", feedback_id)
            raise HTTPException(status_code=404, detail="Feedback not found")
        logger.info("Feedback deleted successfully. Feedback ID: %s", feedback_id)
        return {"message": "Feedback deleted successfully", "feedback_id": feedback_id}
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        handle_database_error("deleting feedback")
