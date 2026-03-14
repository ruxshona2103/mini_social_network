import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

async def create_comment(
    session: AsyncSession,
    comment_in: CommentCreate,
    author_id: uuid.UUID,
    post_id: uuid.UUID
) -> Comment:

    db_comment = Comment(
        content=comment_in.content,
        author_id=author_id,
        post_id=post_id
    )

    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return db_comment

async def get_comments_by_post(
    session: AsyncSession,
    post_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100
) -> list[Comment]:

    stmt = select(Comment).where(Comment.post_id == post_id).offset(skip).limit(limit).order_by(Comment.created_at.asc())
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def get_comment_by_id(session: AsyncSession, comment_id: uuid.UUID) -> Comment | None:
    stmt = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(stmt)
    return result.scalars().first()

async def delete_comment(session: AsyncSession, db_comment: Comment) -> None:
    await session.delete(db_comment)
    await session.commit()