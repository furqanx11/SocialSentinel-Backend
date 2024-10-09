from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel

class user_messagesCreate(BaseModel):
    user_id : int
    message_id : int

class user_messagesUpdate(BaseModel):
    user_id : Optional[int]
    message_id : Optional[int]

class user_messagesRead(BaseSchema):
    user_id : int
    message_id : int