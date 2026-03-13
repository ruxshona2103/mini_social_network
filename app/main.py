import uvicorn
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION
)

@app.get("/")
async def root():
    return {
        "message": "Dastur muvaffaqiyatli ishga tushdi.",
        "swagger_manzili": "http://127.0.0.1:8000/docs"
    }

if __name__ == "__main__":
    # Dasturni 8080-portda ishga tushiramiz
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)