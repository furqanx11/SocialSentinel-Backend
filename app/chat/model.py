from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId


class ChatMessageBase(BaseModel):
    content: str
    sender_id: str
    receiver_id: str
    created_at: datetime = datetime.utcnow()
    
    class Config:
        arbitrary_types_allowed = True

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(BaseModel):
    content: Optional[str]

class ChatMessageFull(ChatMessageBase):
    id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

ChatMessageBase.model_rebuild()
ChatMessageCreate.model_rebuild()
ChatMessageUpdate.model_rebuild()
ChatMessageFull.model_rebuild()