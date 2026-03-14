import uvicorn
from fastapi import FastAPI

from app.core.config import settings
from app.api.endpoints import user, auth, posts, comment, like
import app.models

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION
)

app.include_router(auth.router, tags=["Login"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(comment.router, tags=["Comments"])
app.include_router(like.router, tags=["Likes"])

@app.get("/")
async def root():
    return {
        "message": "Dastur muvaffaqiyatli ishga tushdi.",
        "swagger_manzili": "http://127.0.0.1:8000/docs"
    }

if __name__ == "__main__":
    # Dasturni 8080-portda ishga tushiramiz
    uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)