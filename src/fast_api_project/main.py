# main.py

from fastapi import FastAPI
from fast_api_project.api.v1 import api_router as api_v1_router
from fast_api_project.api.v2 import api_router as api_v2_router
from fast_api_project.core.config import settings

app = FastAPI(title=settings.app.TITLE, version=settings.app.VERSION)
app.include_router(api_v1_router, prefix="/api/v1", tags=["api_v1"])
app.include_router(api_v2_router, prefix="/api/v2", tags=["api_v2"])


@app.get("/")
def show():
    """定義視圖函數"""
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.server.HOST,
        port=settings.server.PORT,
    )