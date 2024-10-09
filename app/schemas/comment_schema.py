from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str]

class CommentRead(BaseSchema):
    content: str
