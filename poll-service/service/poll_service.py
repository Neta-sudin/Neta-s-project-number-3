from typing import List, Optional
from fastapi import HTTPException, status
from model.question import Question, QuestionCreate, QuestionUpdate, QuestionResponse
from model.answer import Answer, AnswerCreate, AnswerUpdate, UserAnswerResponse
from model.statistics import QuestionStatistics, AllQuestionsStatistics
from repository import question_repository, answer_repository
from api.internal_api import user_service_api


async def create_question(question: QuestionCreate) -> int:
    """
    Create a new poll question.
    """
    question_id = await question_repository.create_question(question)
    return question_id


async def get_all_questions() -> List[QuestionResponse]:
    """
    Get all poll questions.
    """
    questions = await question_repository.get_all()
    return [QuestionResponse(**q.dict()) for q in questions]


async def get_question_by_id(question_id: int) -> Optional[QuestionResponse]:
    """
    Get a specific question by ID.
    """
    question = await question_repository.get_by_id(question_id)
    if question:
        return QuestionResponse(**question.dict())
    return None


async def update_question(question_id: int, question_update: QuestionUpdate) -> bool:
    """
    Update an existing question.
    """
    question = await question_repository.get_by_id(question_id)
    if not question:
        return False

    updated = await question_repository.update_question(question_id, question_update)
    return updated


async def delete_question(question_id: int) -> bool:
    """
    Delete a question. This will cascade delete all answers.
    """
    question = await question_repository.get_by_id(question_id)
    if not question:
        return False

    deleted = await question_repository.delete_question(question_id)
    return deleted


async def submit_answer(answer: AnswerCreate) -> int:
    """
    Submit an answer to a question.
    """
    try:
        user_info = await user_service_api.verify_user_registered(answer.user_id)
        if not user_info.get("exists"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {answer.user_id} does not exist"
            )
        if not user_info.get("is_registered"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with id {answer.user_id} is not registered. Only registered users can answer polls."
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot verify user registration: {str(e)}"
        )

    question = await question_repository.get_by_id(answer.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with id {answer.question_id} does not exist"
        )

    existing_answer = await answer_repository.get_by_user_and_question(
        answer.user_id, answer.question_id
    )
    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User {answer.user_id} has already answered question {answer.question_id}. Use update endpoint to change the answer."
        )

    answer_id = await answer_repository.create_answer(answer)
    return answer_id


async def update_answer(user_id: int, question_id: int, answer_update: AnswerUpdate) -> bool:
    """
    Update an existing answer.
    """
    try:
        user_info = await user_service_api.verify_user_registered(user_id)
        if not user_info.get("exists"):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} does not exist"
            )
        if not user_info.get("is_registered"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User with id {user_id} is not registered"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Cannot verify user registration: {str(e)}"
        )

    existing_answer = await answer_repository.get_by_user_and_question(user_id, question_id)
    if not existing_answer:
        return False

    updated = await answer_repository.update_answer(
        user_id, question_id, answer_update.selected_option
    )
    return updated


async def get_question_option_counts(question_id: int) -> Optional[QuestionStatistics]:
    """
    API 1: By question_id → Return how many users choose each of the question options.
    """
    question = await question_repository.get_by_id(question_id)
    if not question:
        return None

    option_counts = await answer_repository.get_option_counts_for_question(question_id)
    total_responses = await answer_repository.count_answers_by_question(question_id)

    return QuestionStatistics(
        question_id=question.id,
        question_title=question.title,
        total_responses=total_responses,
        option_1_count=option_counts["option_1"],
        option_2_count=option_counts["option_2"],
        option_3_count=option_counts["option_3"],
        option_4_count=option_counts["option_4"],
        option_1_text=question.option_1,
        option_2_text=question.option_2,
        option_3_text=question.option_3,
        option_4_text=question.option_4
    )


async def get_question_total_responses(question_id: int) -> Optional[int]:
    """
    API 2: By question_id → Return how many users answer to this question in total.
    """
    question = await question_repository.get_by_id(question_id)
    if not question:
        return None

    total = await answer_repository.count_answers_by_question(question_id)
    return total


async def get_user_answers(user_id: int) -> List[UserAnswerResponse]:
    """
    API 3: By user_id → Return the user answer to each question he submitted.
    """
    answers = await answer_repository.get_answers_by_user(user_id)

    result = []
    for answer in answers:
        question = await question_repository.get_by_id(answer.question_id)
        if question:
            option_text = getattr(question, f"option_{answer.selected_option}")
            result.append(UserAnswerResponse(
                user_id=answer.user_id,
                question_id=question.id,
                question_title=question.title,
                selected_option=answer.selected_option,
                selected_option_text=option_text
            ))

    return result


async def get_user_total_answered(user_id: int) -> int:
    """
    API 4: By user_id → Return how many questions this user answered to in total.
    """
    total = await answer_repository.count_answers_by_user(user_id)
    return total


async def get_all_questions_statistics() -> List[AllQuestionsStatistics]:
    """
    API 5: Return all questions and all possible options and for each question
    return how many users choose each of the question options.
    """
    questions = await question_repository.get_all()

    result = []
    for question in questions:
        option_counts = await answer_repository.get_option_counts_for_question(question.id)
        total_responses = await answer_repository.count_answers_by_question(question.id)

        statistics = {
            question.option_1: option_counts["option_1"],
            question.option_2: option_counts["option_2"],
            question.option_3: option_counts["option_3"],
            question.option_4: option_counts["option_4"]
        }

        result.append(AllQuestionsStatistics(
            question_id=question.id,
            question_title=question.title,
            total_responses=total_responses,
            statistics=statistics
        ))

    return result


async def delete_user_answers(user_id: int) -> bool:
    """
    Delete all answers for a user. Called when user is deleted from User Service.
    """
    return await answer_repository.delete_answers_by_user(user_id)
