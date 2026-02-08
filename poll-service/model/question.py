from typing import Optional
from pydantic import BaseModel, Field


class Question(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=5)
    option_1: str = Field(..., min_length=1, max_length=500)
    option_2: str = Field(..., min_length=1, max_length=500)
    option_3: str = Field(..., min_length=1, max_length=500)
    option_4: str = Field(..., min_length=1, max_length=500)


class QuestionCreate(BaseModel):
    title: str = Field(..., min_length=5)
    option_1: str = Field(..., min_length=1, max_length=500)
    option_2: str = Field(..., min_length=1, max_length=500)
    option_3: str = Field(..., min_length=1, max_length=500)
    option_4: str = Field(..., min_length=1, max_length=500)


class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5)
    option_1: Optional[str] = Field(None, min_length=1, max_length=500)
    option_2: Optional[str] = Field(None, min_length=1, max_length=500)
    option_3: Optional[str] = Field(None, min_length=1, max_length=500)
    option_4: Optional[str] = Field(None, min_length=1, max_length=500)


class QuestionResponse(BaseModel):
    id: int
    title: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str

