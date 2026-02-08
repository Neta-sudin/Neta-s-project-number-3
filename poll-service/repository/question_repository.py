from typing import List, Optional
from model.question import Question, QuestionCreate, QuestionUpdate
from repository.database import database


async def get_by_id(question_id: int) -> Optional[Question]:
    query = "SELECT * FROM questions WHERE id = :question_id"
    result = await database.fetch_one(query, values={"question_id": question_id})
    if result:
        return Question(**dict(result))
    return None


async def get_all() -> List[Question]:
    query = "SELECT * FROM questions ORDER BY id"
    results = await database.fetch_all(query)
    return [Question(**dict(record)) for record in results]


async def create_question(question: QuestionCreate) -> int:
    query = """
        INSERT INTO questions (title, option_1, option_2, option_3, option_4)
        VALUES (:title, :option_1, :option_2, :option_3, :option_4)
    """
    values = {
        "title": question.title,
        "option_1": question.option_1,
        "option_2": question.option_2,
        "option_3": question.option_3,
        "option_4": question.option_4,
    }

    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID() as id")

    return last_record_id["id"]


async def update_question(question_id: int, question: QuestionUpdate) -> bool:
    update_fields = []
    values = {"question_id": question_id}

    if question.title is not None:
        update_fields.append("title = :title")
        values["title"] = question.title
    if question.option_1 is not None:
        update_fields.append("option_1 = :option_1")
        values["option_1"] = question.option_1
    if question.option_2 is not None:
        update_fields.append("option_2 = :option_2")
        values["option_2"] = question.option_2
    if question.option_3 is not None:
        update_fields.append("option_3 = :option_3")
        values["option_3"] = question.option_3
    if question.option_4 is not None:
        update_fields.append("option_4 = :option_4")
        values["option_4"] = question.option_4

    if not update_fields:
        return False

    query = f"UPDATE questions SET {', '.join(update_fields)} WHERE id = :question_id"
    result = await database.execute(query, values)
    return result > 0


async def delete_question(question_id: int) -> bool:
    query = "DELETE FROM questions WHERE id = :question_id"
    result = await database.execute(query, values={"question_id": question_id})
    return result > 0

