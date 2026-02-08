from pydantic import BaseModel, EmailStr, Field
from datetime import date
class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., gt=0, le=120)
    address: str = Field(..., min_length=1, max_length=500)
    joining_date: date
    is_registered: bool = False
