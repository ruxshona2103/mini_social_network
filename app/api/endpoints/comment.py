from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db.database import get_db
from app.crud import comment as crud_comment
from app.crud import posts as crud_post
from app.schemas.comment import CommentCreate, CommentResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment_for_post(
        post_id: uuid.UUID,
        comment_in: CommentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)  # XAVFSIZLIK: Qorovul!
):

    post = await crud_post.get_post_by_id(session=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Kechirasiz, maqola topilmadi")

    new_comment = await crud_comment.create_comment(
        session=db,
        comment_in=comment_in,
        author_id=current_user.id,
        post_id=post_id
    )
    return new_comment


@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
async def read_comments_for_post(
        post_id: uuid.UUID,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):

    post = await crud_post.get_post_by_id(session=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Maqola topilmadi")

    comments = await crud_comment.get_comments_by_post(session=db, post_id=post_id, skip=skip, limit=limit)
    return comments


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_comment(
        comment_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)  # XAVFSIZLIK: Qorovul!
):

    comment = await crud_comment.get_comment_by_id(session=db, comment_id=comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Izoh topilmadi")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ruxsat etilmagan! Faqat o'zingizning izohingizni o'chira olasiz.")

    await crud_comment.delete_comment(session=db, db_comment=comment)
    return None