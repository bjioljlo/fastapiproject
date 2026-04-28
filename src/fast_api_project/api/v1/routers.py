# routers.py

from fastapi import APIRouter
from .endpoints import blog_router, questions_router

api_router = APIRouter()
api_router.include_router(questions_router, prefix="/questions")
api_router.include_router(blog_router, prefix="/blog")