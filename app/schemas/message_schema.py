from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class MessageCreate(BaseModel):
    content: str

class MessageUpdate(BaseModel):
    content: Optional[str]

class MessageRead(BaseSchema):
    content: str
