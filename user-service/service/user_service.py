from typing import List, Optional
from fastapi import HTTPException, status
from model.user import User
from model.user_create import UserCreate
from model.user_update import UserUpdate
from model.user_response import UserResponse
from repository import user_repository
from api.internal_api import poll_service_api


async def get_by_id(user_id: int) -> Optional[User]:
    user = await user_repository.get_by_id(user_id)
    if not user:
        return None
    return user


async def get_all() -> List[User]:
    return await user_repository.get_all()


async def create_user(user: UserCreate) -> int:
    try:
        user_id = await user_repository.create_user(user)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )


async def update_user(user_id: int, user: UserUpdate) -> bool:
    existing_user = await user_repository.get_by_id(user_id)
    if not existing_user:
        return False

    updated = await user_repository.update_user(user_id, user)
    return updated


async def delete_user(user_id: int) -> bool:
    existing_user = await user_repository.get_by_id(user_id)
    if not existing_user:
        return False

    await poll_service_api.delete_user_answers(user_id)

    deleted = await user_repository.delete_user(user_id)
    return deleted


async def register_user(user_id: int, is_registered: bool) -> bool:
    existing_user = await user_repository.get_by_id(user_id)
    if not existing_user:
        return False

    updated = await user_repository.register_user(user_id, is_registered)
    return updated


async def check_user_registered(user_id: int) -> Optional[bool]:
    """
    Check if user exists and is registered.
    Returns True if registered, False if not registered, None if user doesn't exist.
    """
    return await user_repository.check_user_registered(user_id)

