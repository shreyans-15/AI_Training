from sqlalchemy import Boolean, Column, Date, Integer, String
from config.database import Base

class TrainingFeedback(Base):
    __tablename__ = "TrainingFeedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    learner_name = Column(String(100), nullable=False)
    trainer_name = Column(String(100), nullable=False)
    course_name = Column(String(150), nullable=False)
    session_date = Column(Date, nullable=False)
    content_rating = Column(Integer, nullable=False)
    trainer_rating = Column(Integer, nullable=False)
    hands_on_rating = Column(Integer, nullable=False)
    comments = Column(String(1000), nullable=True)
    would_recommend = Column(Boolean, nullable=False)
