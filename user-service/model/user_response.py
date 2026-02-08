from pydantic import BaseModel
from datetime import date
class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    age: int
    address: str
    joining_date: date
    is_registered: bool
