from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.crud import user as crud_user
from app.db.database import get_db
from app.api.deps import get_current_user


router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # email bandmi yo bandmasmi shuni tekshiramiz -- egde case
    user_by_email = await crud_user.get_user_by_email(db, email=user_in.email)
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email bilan allaqachon ro'yxatdan o'tilgan!!!",
        )

    user_by_username = await crud_user.get_user_by_username(db, username=user_in.username)
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username bilan allaqachon ro'yxatdan o'tilgan!!!",
        )

    new_user = await crud_user.create_user(db, user_in=user_in)
    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tizimda kutilmagan xatolik yuz berdi, qayta urinib koring."
        )
    return new_user

@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user