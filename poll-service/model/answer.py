from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Answer(BaseModel):
    id: Optional[int] = None
    user_id: int
    question_id: int
    selected_option: int = Field(..., ge=1, le=4)


class AnswerCreate(BaseModel):
    user_id: int
    question_id: int
    selected_option: int = Field(..., ge=1, le=4, description="Must be between 1 and 4")


class AnswerUpdate(BaseModel):
    selected_option: int = Field(..., ge=1, le=4, description="Must be between 1 and 4")


class AnswerResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    selected_option: int
    question_title: Optional[str] = None
    selected_option_text: Optional[str] = None


class UserAnswerResponse(BaseModel):
    user_id: int
    question_id: int
    question_title: str
    selected_option: int
    selected_option_text: str

