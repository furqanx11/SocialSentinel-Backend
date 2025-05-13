from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PostStatus(str, Enum):
    active = "active"
    under_review = "under_review"
    blocked = "blocked"

class PostBase(BaseModel):
    content: str
    author_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    class Config:
        arbitrary_types_allowed = True

class PostCreate(PostBase):
    status:PostStatus = PostStatus.active

class PostUpdate(BaseModel):
    content: Optional[str]
    status: Optional[PostStatus]
    updated_at: datetime = datetime.utcnow()

class PostFull(PostBase):
    id: str
    likes: int = 0
    comments: List[str] = []
    status: PostStatus
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

PostBase.model_rebuild()
PostCreate.model_rebuild()
PostUpdate.model_rebuild()
PostFull.model_rebuild()