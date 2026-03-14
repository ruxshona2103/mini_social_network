import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.like import Like


async def toggle_like(session: AsyncSession, user_id: uuid.UUID, post_id: uuid.UUID) -> dict:
    # 1. Avval shu mijoz shu postga layk bosganmi, shuni qidiramiz
    stmt = select(Like).where(Like.user_id == user_id, Like.post_id == post_id)
    result = await session.execute(stmt)
    existing_like = result.scalars().first()

    if existing_like:
        # 2. Agar layk topilsa, demak u qaytarib olyapti (Unlike)
        await session.delete(existing_like)
        await session.commit()
        return {"status": "unliked", "message": "Layk qaytarib olindi"}
    else:
        # 3. Agar layk topilmasa, demak yangi layk bosyapti (Like)
        new_like = Like(user_id=user_id, post_id=post_id)
        session.add(new_like)
        await session.commit()
        return {"status": "liked", "message": "Layk bosildi"}