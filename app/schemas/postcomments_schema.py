from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class PostCommentCreate(BaseModel):
    post_id : int
    user_id : int
    comment_id : int

class PostCommentUpdate(BaseModel):
    post_id : Optional[int]
    user_id : Optional[int]
    comment_id : Optional[int]

class PostCommentRead(BaseSchema):
    post_id : int
    user_id : int
    comment_id : int