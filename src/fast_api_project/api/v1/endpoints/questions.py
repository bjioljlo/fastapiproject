# questions.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fast_api_project.core.database import SessionLocal
from fast_api_project.models import Question

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

@router.get("/{question_id}")
async def get_a_question(question_id: int, db: Session = db_dependency):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="This id's is not found...")
    return question
