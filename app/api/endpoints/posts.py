import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud import posts as crud_post
from app.schemas.post import PostCreate, PostResponse, PostUpdate
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_post = await crud_post.create_post(session=db, post_in=post_in, author_id=current_user.id)
    return new_post

@router.get("/", response_model=list[PostResponse])
async def read_all_posts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):

    posts = await crud_post.get_all_posts(session=db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=PostResponse)
async def read_single_post(
    post_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):

    post = await crud_post.get_post_by_id(session=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Kechirasiz, bunday post topilmadi")
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_existing_post(
        post_id: uuid.UUID,
        post_in: PostUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    post = await crud_post.get_post_by_id(session=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Kechirasiz, bunday post topilmadi")

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ruxsat etilmagan amal! Siz faqat o'zingizning postingizni o'zgartira olasiz."
        )

    updated_post = await crud_post.update_post(session=db, db_post=post, post_in=post_in)
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
        post_id: uuid.UUID,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):

    post = await crud_post.get_post_by_id(session=db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Kechirasiz, bunday post topilmadi")

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Ruxsat etilmagan amal! Siz faqat o'zingizning postingizni o'chira olasiz."
        )

    await crud_post.delete_post(session=db, db_post=post)
    return None