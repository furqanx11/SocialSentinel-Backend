from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    blocked = "blocked"
    under_review = "under_review"

class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    status:UserStatus = UserStatus.active
    active_now: bool = True
    last_active: datetime = Field(default_factory=datetime.utcnow)
    fairness_score: float = 0.0
    warnings: int = 0
    is_blocked: bool = False
    friends: Optional[list[str]] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserSignUp(UserBase):
    pass

class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    class Config:
        arbitrary_types_allowed = True

class UserUpdate(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    fainess_score: Optional[float]
    warnings: Optional[int]
    is_blocked: Optional[bool]
    status: Optional[UserStatus]
    friends: Optional[list[str]] = None

    class Config:
        arbitrary_types_allowed = True

class UserFull(UserBase):
    id : str

    class Config:
        arbitrary_types_allowed = True

class UserFriends(BaseModel):
    user_id:str
    friend_ids: list[str]

UserBase.model_rebuild()
UserSignUp.model_rebuild()
UserLogin.model_rebuild()
UserUpdate.model_rebuild()
UserFull.model_rebuild()
