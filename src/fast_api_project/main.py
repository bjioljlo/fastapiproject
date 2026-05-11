# main.py

from fastapi import FastAPI
from fast_api_project.api.v1 import api_router as api_v1_router
from fast_api_project.api.v2 import api_router as api_v2_router

app = FastAPI(title="OH~MY~~API", version="1.0.0")
app.include_router(api_v1_router, prefix="/api/v1", tags=["api_v1"])
app.include_router(api_v2_router, prefix="/api/v2", tags=["api_v2"])

@app.get("/")
def show():
    """定義視圖函數"""
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
