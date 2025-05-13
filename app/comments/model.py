from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class CommentStatus(str, Enum):
    active = "active"
    under_review = "under_review"
    blocked = "blocked"

class CommentBase(BaseModel):
    content: str
    author_id: str
    post_id: str
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CommentCreate(CommentBase):
    status: CommentStatus = CommentStatus.active

class CommentUpdate(BaseModel):
    content: Optional[str]
    status: Optional[CommentStatus]
    updated_at: datetime = datetime.utcnow()

    class Config:
        arbitrary_types_allowed = True

class CommentFull(CommentBase):
    id: str
    status: CommentStatus
    username: Optional[str] = None
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

CommentBase.model_rebuild()
CommentCreate.model_rebuild()
CommentUpdate.model_rebuild()
CommentFull.model_rebuild()