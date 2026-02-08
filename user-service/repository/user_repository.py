from typing import List, Optional
from model.user import User
from model.user_create import UserCreate
from model.user_update import UserUpdate
from model.user_response import UserResponse
from repository.database import database


async def get_by_id(user_id: int) -> Optional[User]:
    query = "SELECT * FROM users WHERE id = :user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return User(**dict(result))
    return None


async def get_all() -> List[User]:
    query = "SELECT * FROM users ORDER BY id"
    results = await database.fetch_all(query)
    return [User(**dict(record)) for record in results]


async def create_user(user: UserCreate) -> int:
    query = """
        INSERT INTO users (first_name, last_name, email, age, address, joining_date, is_registered)
        VALUES (:first_name, :last_name, :email, :age, :address, :joining_date, :is_registered)
    """
    values = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "address": user.address,
        "joining_date": user.joining_date,
        "is_registered": user.is_registered,
    }

    async with database.transaction():
        await database.execute(query, values)
        last_record_id = await database.fetch_one("SELECT LAST_INSERT_ID() as id")

    return last_record_id["id"]


async def update_user(user_id: int, user: UserUpdate) -> bool:
    update_fields = []
    values = {"user_id": user_id}

    if user.first_name is not None:
        update_fields.append("first_name = :first_name")
        values["first_name"] = user.first_name
    if user.last_name is not None:
        update_fields.append("last_name = :last_name")
        values["last_name"] = user.last_name
    if user.email is not None:
        update_fields.append("email = :email")
        values["email"] = user.email
    if user.age is not None:
        update_fields.append("age = :age")
        values["age"] = user.age
    if user.address is not None:
        update_fields.append("address = :address")
        values["address"] = user.address
    if user.joining_date is not None:
        update_fields.append("joining_date = :joining_date")
        values["joining_date"] = user.joining_date
    if user.is_registered is not None:
        update_fields.append("is_registered = :is_registered")
        values["is_registered"] = user.is_registered

    if not update_fields:
        return False

    query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = :user_id"
    result = await database.execute(query, values)
    return result > 0


async def delete_user(user_id: int) -> bool:
    query = "DELETE FROM users WHERE id = :user_id"
    result = await database.execute(query, values={"user_id": user_id})
    return result > 0


async def register_user(user_id: int, is_registered: bool) -> bool:
    query = "UPDATE users SET is_registered = :is_registered WHERE id = :user_id"
    result = await database.execute(query, values={"user_id": user_id, "is_registered": is_registered})
    return result > 0


async def check_user_registered(user_id: int) -> Optional[bool]:
    query = "SELECT is_registered FROM users WHERE id = :user_id"
    result = await database.fetch_one(query, values={"user_id": user_id})
    if result:
        return result["is_registered"]
    return None

