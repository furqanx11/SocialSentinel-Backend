from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class UserPostCreate(BaseModel):
    user_id : int
    post_id : int

class UserPostUpdate(BaseModel):
    user_id : Optional[int]
    post_id : Optional[int]

class UserPostRead(BaseSchema):
    user_id : int
    post_id : int

