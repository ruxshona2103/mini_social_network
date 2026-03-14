import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.crud import user as crud_user
from app.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.ALGORITHMS
        )

        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=401, detail="Tokenda ID topilmadi")

        try:
            user_id = uuid.UUID(user_id_str)
        except ValueError:
            raise HTTPException(status_code=401, detail="Token ichidagi ID formati noto'g'ri (UUID emas)")

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz yoki muddati tugagan. Qaytadan login qiling.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")

    return user
