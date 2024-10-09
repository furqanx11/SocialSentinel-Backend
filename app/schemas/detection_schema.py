from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DetectionCreate(BaseModel):
    post_id: Optional[int]
    comment_id: Optional[int]
    message_id: Optional[int]
    model_name: str
    score: float
    reason: str

class DetectionRead(BaseSchema):
    post_id: Optional[int]
    comment_id: Optional[int]
    message_id: Optional[int]
    model_name: str
    score: float
    reason: str

class DetectionUpdate(BaseModel):
    model_name: Optional[str]
    score: Optional[float]
    reason: Optional[str]

class FlaggedPost(BaseModel):
    
    post_id: int
    content: str
    reason: str
    model_name: str
    score: float
    timestamp: datetime

class FlaggedComment(BaseModel):
    comment_id: int
    content: str
    reason: str
    model_name: str
    score: float
    timestamp: datetime

class FlaggedMessage(BaseModel):
    message_id: int
    content: str
    reason: str
    model_name: str
    score: float
    timestamp: datetime

class CreateFlaggedContent(BaseModel):
    model_name: str
    score: float
    reason: str
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    message_id: Optional[int] = None