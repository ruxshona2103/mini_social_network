import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr , ConfigDict, Field


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: str = Field(..., min_length=3, max_length=255)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50, description="Parol kamida 6 ta belgidan iborat bo'lishi kerak")

class UserResponse(UserBase):
    id: uuid.UUID
    is_verified: bool
    created_at: datetime

    # SQLAlchemy modelini Pydantic tushunishi uchun sozlama
    model_config = ConfigDict(from_attributes=True)