from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalars().first()

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    return result.scalars().first()

async def create_user(session: AsyncSession, user_in: UserCreate) -> User | None:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email= user_in.email,
        username= user_in.username,
        full_name= user_in.full_name,
        password_hash= hashed_password,
    )

    session.add(db_user)

    try:
        await session.commit()
        await session.refresh(db_user)
        return db_user

    except IntegrityError:
        await session.rollback()
        return None


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()
