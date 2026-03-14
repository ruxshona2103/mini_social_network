import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    content: str = Field(..., min_length=10)

# Mijoz faqat sarlavha va matn yuboradi
class PostCreate(PostBase):
    pass  


class PostResponse(PostBase):
    id: uuid.UUID
    author_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None