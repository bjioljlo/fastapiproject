# blog.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/{id}")
async def get_blog(id: int):
    return {"data": f"Blog 的 id 是：{id}"}

@router.get("/{id}/{comments}")
async def get_comment(id, comments: int):
    return {"data": { "id": id, "comments": f"Blog 的 comments 是：{comments}"}}