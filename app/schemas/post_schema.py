from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class PostCreate(BaseModel):
    content: str

class PostUpdate(BaseModel):
    content: Optional[str]

class PostRead(BaseSchema):
    content: str
