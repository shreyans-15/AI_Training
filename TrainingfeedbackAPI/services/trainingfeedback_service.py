from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from models.trainingfeedback_model import TrainingFeedback
from schemas.trainingfeedback_schema import TrainingFeedbackCreate, TrainingFeedbackUpdate

def create_feedback(db: Session, feedback: TrainingFeedbackCreate):
    db_feedback = TrainingFeedback(**feedback.model_dump())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_all_feedback(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TrainingFeedback).order_by(TrainingFeedback.feedback_id).offset(skip).limit(limit).all()

def get_feedback_by_id(db: Session, feedback_id: int):
    return db.query(TrainingFeedback).filter(TrainingFeedback.feedback_id == feedback_id).first()

def update_feedback(db: Session, feedback_id: int, feedback_data: TrainingFeedbackUpdate):
    db_feedback = get_feedback_by_id(db, feedback_id)
    if db_feedback is None:
        return None
    update_data = feedback_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_feedback, key, value)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int):
    db_feedback = get_feedback_by_id(db, feedback_id)
    if db_feedback is None:
        return None
    db.delete(db_feedback)
    db.commit()
    return db_feedback

def get_feedback_by_trainer(db: Session, trainer_name: str):
    return db.query(TrainingFeedback).filter(TrainingFeedback.trainer_name.ilike(trainer_name)).all()

def get_feedback_by_course(db: Session, course_name: str):
    return db.query(TrainingFeedback).filter(TrainingFeedback.course_name.ilike(course_name)).all()

def get_average_trainer_ratings(db: Session):
    return (
        db.query(
            TrainingFeedback.trainer_name.label("trainer_name"),
            func.avg(TrainingFeedback.trainer_rating).label("average_trainer_rating"),
        )
        .group_by(TrainingFeedback.trainer_name)
        .order_by(TrainingFeedback.trainer_name)
        .all()
    )

def get_low_rated_sessions(db: Session):
    return db.query(TrainingFeedback).filter(
        or_(
            TrainingFeedback.content_rating <= 2,
            TrainingFeedback.trainer_rating <= 2,
            TrainingFeedback.hands_on_rating <= 2,
        )
    ).all()

def get_recommendation_percentage(db: Session, course_name: str):
    total = db.query(func.count(TrainingFeedback.feedback_id)).filter(
        TrainingFeedback.course_name.ilike(course_name)
    ).scalar() or 0

    recommended = db.query(func.count(TrainingFeedback.feedback_id)).filter(
        TrainingFeedback.course_name.ilike(course_name),
        TrainingFeedback.would_recommend.is_(True),
    ).scalar() or 0

    percentage = (recommended / total * 100) if total else 0.0
    return {
        "course_name": course_name,
        "total_feedback": total,
        "recommendations": recommended,
        "recommendation_percentage": round(percentage, 2),
    }
