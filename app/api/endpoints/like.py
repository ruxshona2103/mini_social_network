from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db.database import get_db
from app.crud import like as crud_like
from app.crud import posts as crud_post
from app.schemas.like import LikeToggleResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/posts/{post_id}/like", response_model=LikeToggleResponse, status_code=status.HTTP_200_OK)
async def toggle_like_for_post(
        post_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    # 1. Post borligini tekshiramiz
    post = await crud_post.get_post_by_id(session=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Kechirasiz, maqola topilmadi")

    # 2. Laykni yoqish yoki o'chirish (Toggle) amaliyotini bajaramiz
    result = await crud_like.toggle_like(session=db, user_id=current_user.id, post_id=post_id)
    return result