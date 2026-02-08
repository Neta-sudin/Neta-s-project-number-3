from typing import List, Optional
from model.answer import Answer, AnswerCreate
from repository.database import database


async def get_by_id(answer_id: int) -> Optional[Answer]:
    query = "SELECT * FROM answers WHERE id = :answer_id"
    result = await database.fetch_one(query, values={"answer_id": answer_id})
    if result:
        return Answer(**dict(result))
    return None


async def get_by_user_and_question(user_id: int, question_id: int) -> Optional[Answer]:
    query = """
            SELECT *
            FROM answers
            WHERE user_id = :user_id
              AND question_id = :question_id \
            """
    result = await database.fetch_one(query, values={"user_id": user_id, "question_id": question_id})
    if result:
        return Answer(**dict(result))
    return None


async def get_all_answers() -> List[Answer]:
    query = "SELECT * FROM answers ORDER BY id"
    results = await database.fetch_all(query)
    return [Answer(**dict(record)) for record in results]


async def get_answers_by_user(user_id: int) -> List[Answer]:
    query = "SELECT * FROM answers WHERE user_id = :user_id ORDER BY question_id"
    results = await database.fetch_all(query, values={"user_id": user_id})
    return [Answer(**dict(record)) for record in results]


async def get_answers_by_question(question_id: int) -> List[Answer]:
    query = "SELECT * FROM answers WHERE question_id = :question_id"
    results = await database.fetch_all(query, values={"question_id": question_id})
    return [Answer(**dict(record)) for record in results]


async def create_answer(answer: AnswerCreate) -> int:
    query = """
            INSERT INTO answers (user_id, question_id, selected_option)
            VALUES (:user_id, :question_id, :selected_option) \
            """
    values = {
        "user_id": answer.user_id,
        "question_id": answer.question_id,
        "selected_option": answer.selected_option,
    }

    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID() as id")

    return last_record_id["id"]


async def update_answer(user_id: int, question_id: int, selected_option: int) -> bool:
    query = """
            UPDATE answers
            SET selected_option = :selected_option
            WHERE user_id = :user_id
              AND question_id = :question_id \
            """
    values = {
        "user_id": user_id,
        "question_id": question_id,
        "selected_option": selected_option,
    }
    result = await database.execute(query, values)
    return result > 0


async def delete_answer(answer_id: int) -> bool:
    query = "DELETE FROM answers WHERE id = :answer_id"
    result = await database.execute(query, values={"answer_id": answer_id})
    return result > 0


async def delete_answers_by_user(user_id: int) -> bool:
    query = "DELETE FROM answers WHERE user_id = :user_id"
    await database.execute(query, values={"user_id": user_id})
    return True


async def count_answers_by_user(user_id: int) -> int:
    query = "SELECT COUNT(*) as count FROM answers WHERE user_id = :user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    return result["count"]


async def count_answers_by_question(question_id: int) -> int:
    query = "SELECT COUNT(*) as count FROM answers WHERE question_id = :question_id"
    result = await database.fetch_one(query, values={"question_id": question_id})
    return result["count"]


async def get_option_counts_for_question(question_id: int) -> dict:
    """
    Get count of users who selected each option for a specific question.
    Returns dict with keys 'option_1', 'option_2', 'option_3', 'option_4'
    """
    query = """
            SELECT selected_option,
                   COUNT(*) as count
            FROM answers
            WHERE question_id = :question_id
            GROUP BY selected_option \
            """
    results = await database.fetch_all(query, values={"question_id": question_id})

    counts = {"option_1": 0, "option_2": 0, "option_3": 0, "option_4": 0}

    for record in results:
        option_key = f"option_{record['selected_option']}"
        counts[option_key] = record["count"]

    return counts
