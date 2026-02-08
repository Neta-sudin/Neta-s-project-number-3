from typing import List
from fastapi import APIRouter, HTTPException, status
from model.question import QuestionCreate, QuestionUpdate, QuestionResponse
from model.answer import AnswerCreate, AnswerUpdate, UserAnswerResponse
from model.statistics import QuestionStatistics, AllQuestionsStatistics, UserStatistics
from service import poll_service

router = APIRouter(tags=["polls"])


@router.post("/questions/create", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(question: QuestionCreate):
    """
    Create a new poll question with 4 options.
    """
    question_id = await poll_service.create_question(question)
    created_question = await poll_service.get_question_by_id(question_id)
    return created_question


@router.get("/questions", response_model=List[QuestionResponse], status_code=status.HTTP_200_OK)
async def get_all_questions():
    """
    Get all poll questions.
    """
    questions = await poll_service.get_all_questions()
    return questions


@router.get("/questions/{question_id}", response_model=QuestionResponse, status_code=status.HTTP_200_OK)
async def get_question(question_id: int):
    """
    Get a specific question by ID.
    """
    question = await poll_service.get_question_by_id(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )
    return question


@router.put("/questions/{question_id}", response_model=QuestionResponse, status_code=status.HTTP_200_OK)
async def update_question(question_id: int, question_update: QuestionUpdate):
    """
    Update an existing question.
    """
    updated = await poll_service.update_question(question_id, question_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )
    return await poll_service.get_question_by_id(question_id)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int):
    """
    Delete a question. This will also delete all answers associated with this question.
    """
    deleted = await poll_service.delete_question(question_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )


@router.post("/answers", status_code=status.HTTP_201_CREATED)
async def submit_answer(answer: AnswerCreate):
    """
    Submit an answer to a question.
    User can only answer each question once.
    Only registered users can submit answers.
    """
    answer_id = await poll_service.submit_answer(answer)
    return {
        "message": "Answer submitted successfully",
        "answer_id": answer_id,
        "user_id": answer.user_id,
        "question_id": answer.question_id,
        "selected_option": answer.selected_option
    }


@router.put("/answers/{user_id}/{question_id}", status_code=status.HTTP_200_OK)
async def update_answer(user_id: int, question_id: int, answer_update: AnswerUpdate):
    """
    Update an existing answer.
    User can change their answer to a question they already answered.
    """
    updated = await poll_service.update_answer(user_id, question_id, answer_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Answer not found for user {user_id} and question {question_id}"
        )
    return {
        "message": "Answer updated successfully",
        "user_id": user_id,
        "question_id": question_id,
        "selected_option": answer_update.selected_option
    }


@router.get("/statistics/questions/{question_id}/option-counts", response_model=QuestionStatistics,
            status_code=status.HTTP_200_OK)
async def get_question_option_counts(question_id: int):
    """
    API 1: By passing the question id → Return how many users choose each of the question options.
    Shows breakdown of how many users selected each option (1, 2, 3, or 4).
    """
    statistics = await poll_service.get_question_option_counts(question_id)
    if not statistics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )
    return statistics


@router.get("/statistics/questions/{question_id}/total-responses", status_code=status.HTTP_200_OK)
async def get_question_total_responses(question_id: int):
    """
    API 2: By passing the question id → Return how many users answer to this question in total.
    Returns the total count of users who answered this question.
    """
    total = await poll_service.get_question_total_responses(question_id)
    if total is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {question_id} not found"
        )
    return {
        "question_id": question_id,
        "total_responses": total
    }


@router.get("/statistics/users/{user_id}/answers", response_model=List[UserAnswerResponse],
            status_code=status.HTTP_200_OK)
async def get_user_answers(user_id: int):
    """
    API 3: By passing the user id → Return the user answer to each question he submitted.
    Shows all questions answered by this user with their selected options.
    """
    answers = await poll_service.get_user_answers(user_id)
    return answers


@router.get("/statistics/users/{user_id}/total-answered", response_model=UserStatistics, status_code=status.HTTP_200_OK)
async def get_user_total_answered(user_id: int):
    """
    API 4: By passing the user id → Return how many questions this user answered to in total.
    Returns the count of questions answered by this user.
    """
    total = await poll_service.get_user_total_answered(user_id)
    return UserStatistics(
        user_id=user_id,
        total_questions_answered=total
    )


@router.get("/statistics/all-questions", response_model=List[AllQuestionsStatistics], status_code=status.HTTP_200_OK)
async def get_all_questions_statistics():
    """
    API 5: Return all questions and all possible options and for each question
    return how many users choose each of the question options.
    Comprehensive view of all questions with option counts.
    """
    statistics = await poll_service.get_all_questions_statistics()
    return statistics


@router.delete("/internal/users/{user_id}/answers", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_answers(user_id: int):
    """
    Internal endpoint: Delete all answers for a user.
    Called by User Service when a user is deleted.
    """
    await poll_service.delete_user_answers(user_id)
