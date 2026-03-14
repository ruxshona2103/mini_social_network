import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.posts import Post
from app.schemas.post import PostCreate, PostUpdate

async def create_post(session: AsyncSession, post_in: PostCreate, author_id: uuid.UUID) -> Post:
    db_post = Post(
        title= post_in.title,
        content= post_in.content,
        author_id = author_id
    )
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post

async def get_all_posts(session: AsyncSession, skip: int=0, limit: int=100) -> list[Post]:
    stmt = select(Post).offset(skip).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_post_by_id(session: AsyncSession, post_id: uuid.UUID) -> Post| None:
    stmt = select(Post).where(Post.id == post_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_post(session: AsyncSession, db_post: Post, post_in: PostUpdate) -> Post:
    update_data = post_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_post, field, value)

    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post


async def delete_post(session: AsyncSession, db_post: Post) -> None:
    await session.delete(db_post)
    await session.commit()