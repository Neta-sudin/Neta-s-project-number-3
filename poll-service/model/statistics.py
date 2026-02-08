from pydantic import BaseModel
from typing import Dict


class QuestionStatistics(BaseModel):
    question_id: int
    question_title: str
    total_responses: int
    option_1_count: int
    option_2_count: int
    option_3_count: int
    option_4_count: int
    option_1_text: str
    option_2_text: str
    option_3_text: str
    option_4_text: str


class AllQuestionsStatistics(BaseModel):
    question_id: int
    question_title: str
    total_responses: int
    statistics: Dict[str, int]


class UserStatistics(BaseModel):
    user_id: int
    total_questions_answered: int



