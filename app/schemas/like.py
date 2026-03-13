import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict

# Layk bosish uchun foydalanuvchidan hech qanday matn kutmaymiz,
# shuning uchun Base va Create sxemalari shart emas.

class LikeResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    post_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)