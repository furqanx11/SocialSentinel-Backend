from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Common base schema
class BaseSchema(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
