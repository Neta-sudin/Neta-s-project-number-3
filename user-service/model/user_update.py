from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import date
class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0, le=120)
    address: Optional[str] = Field(None, min_length=1, max_length=500)
    joining_date: Optional[date] = None
    is_registered: Optional[bool] = None
