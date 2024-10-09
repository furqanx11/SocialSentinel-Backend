from app.schemas.base_schema import BaseSchema
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = 'user'

class UserUpdate(BaseModel):
    name: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    role: Optional[str]
    is_active: Optional[bool]

class UserRead(BaseSchema):
    name: str
    username: str
    email: EmailStr
    role: str
    is_active: bool
