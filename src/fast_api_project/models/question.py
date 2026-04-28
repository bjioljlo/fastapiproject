# models/question.py

from sqlalchemy import Column, Integer, String, Boolean
from ..core.database import Base

class Question(Base):
    __tablename__ = "Questions"
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String)
    answer = Column(String)
    is_correct = Column(Boolean)