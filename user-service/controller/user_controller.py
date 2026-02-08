from typing import List
from fastapi import APIRouter, HTTPException, status
from model.user import User
from model.user_create import UserCreate
from model.user_update import UserUpdate
from model.user_response import UserResponse
from service import user_service

router = APIRouter(prefix="/users", tags=["users"]
                   )


@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users():
    users = await user_service.get_all()
    return users


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int):
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.post("/create-user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user_id = await user_service.create_user(user)
    created_user = await user_service.get_by_id(user_id)
    return created_user


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserUpdate):
    updated = await user_service.update_user(user_id, user)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    updated_user = await user_service.get_by_id(user_id)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


@router.post("/{user_id}/register", response_model=dict, status_code=status.HTTP_200_OK)
async def register_user(user_id: int, is_registered: bool = True):
    """
    Register or unregister a user. Only registered users can answer polls.
    """
    updated = await user_service.register_user(user_id, is_registered)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return {
        "message": f"User {user_id} {'registered' if is_registered else 'unregistered'} successfully",
        "is_registered": is_registered
    }


@router.get("/{user_id}/verify", response_model=dict, status_code=status.HTTP_200_OK)
async def verify_user_registration(user_id: int):
    """
    Verify if a user exists and is registered. Used by Poll Service.
    """
    is_registered = await user_service.check_user_registered(user_id)
    if is_registered is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return {
        "user_id": user_id,
        "exists": True,
        "is_registered": is_registered
    }
